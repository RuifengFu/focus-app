use chrono::{Duration, Local};
use serde::{Deserialize, Serialize};
use serde_json::json;
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::Mutex;

#[derive(Serialize, Deserialize)]
pub struct TimerStatus {
    is_running: bool,
    is_break: bool,
    remaining_seconds: i64,
    total_seconds: i64,
    completed_pomodoros: u64,
}

pub struct PomodoroTimer {
    work_duration: Mutex<Duration>,
    break_duration: Mutex<Duration>,
    is_running: AtomicBool,
    is_break: AtomicBool,
    start_time: AtomicU64,
    elapsed_time: AtomicU64,
    completed_pomodoros: AtomicU64,
    work_time_today: AtomicU64,
    work_time_start: AtomicU64,
    daily_work_hours: AtomicU64,
}

impl PomodoroTimer {
    pub fn new() -> Self {
        Self {
            work_duration: Mutex::new(Duration::minutes(25)),
            break_duration: Mutex::new(Duration::minutes(5)),
            is_running: AtomicBool::new(false),
            is_break: AtomicBool::new(false),
            start_time: AtomicU64::new(0),
            elapsed_time: AtomicU64::new(0),
            completed_pomodoros: AtomicU64::new(0),
            work_time_today: AtomicU64::new(0),
            work_time_start: AtomicU64::new(0),
            daily_work_hours: AtomicU64::new(8),
        }
    }
    
    pub fn start(&self) -> serde_json::Value {
        let now = Local::now().timestamp() as u64;
        self.start_time.store(now, Ordering::SeqCst);
        self.is_running.store(true, Ordering::SeqCst);
        
        if !self.is_break.load(Ordering::SeqCst) {
            self.work_time_start.store(now, Ordering::SeqCst);
        }
        
        self.get_status()
    }
    
    pub fn pause(&self) -> serde_json::Value {
        if self.is_running.load(Ordering::SeqCst) {
            let now = Local::now().timestamp() as u64;
            let start = self.start_time.load(Ordering::SeqCst);
            let new_elapsed = now - start + self.elapsed_time.load(Ordering::SeqCst);
            self.elapsed_time.store(new_elapsed, Ordering::SeqCst);
            
            if !self.is_break.load(Ordering::SeqCst) {
                let work_start = self.work_time_start.load(Ordering::SeqCst);
                let work_time = now - work_start;
                self.work_time_today.fetch_add(work_time, Ordering::SeqCst);
            }
            
            self.is_running.store(false, Ordering::SeqCst);
        }
        self.get_status()
    }
    
    pub fn reset(&self) -> serde_json::Value {
        if self.is_running.load(Ordering::SeqCst) && !self.is_break.load(Ordering::SeqCst) {
            let now = Local::now().timestamp() as u64;
            let work_start = self.work_time_start.load(Ordering::SeqCst);
            let work_time = now - work_start;
            self.work_time_today.fetch_add(work_time, Ordering::SeqCst);
        }
        
        self.is_running.store(false, Ordering::SeqCst);
        self.elapsed_time.store(0, Ordering::SeqCst);
        self.get_status()
    }
    
    pub fn update_settings(&self, work_time_minutes: u64, break_time_minutes: u64, daily_work_hours: u64) -> serde_json::Value {
        let was_running = self.is_running.load(Ordering::SeqCst);
        if was_running {
            self.pause();
        }
        
        {
            let mut work_duration = self.work_duration.lock().unwrap();
            *work_duration = Duration::minutes(work_time_minutes as i64);
        }
        
        {
            let mut break_duration = self.break_duration.lock().unwrap();
            *break_duration = Duration::minutes(break_time_minutes as i64);
        }
        
        self.daily_work_hours.store(daily_work_hours, Ordering::SeqCst);
        
        self.elapsed_time.store(0, Ordering::SeqCst);
        
        if was_running {
            self.start();
        }
        
        self.get_status()
    }
    
    pub fn get_status(&self) -> serde_json::Value {
        let is_running = self.is_running.load(Ordering::SeqCst);
        let is_break = self.is_break.load(Ordering::SeqCst);
        let completed_pomodoros = self.completed_pomodoros.load(Ordering::SeqCst);
        
        let current_duration = if is_break {
            *self.break_duration.lock().unwrap()
        } else {
            *self.work_duration.lock().unwrap()
        };
        
        let total_seconds = current_duration.num_seconds();
        
        let elapsed_seconds = if is_running {
            let now = Local::now().timestamp() as u64;
            let start = self.start_time.load(Ordering::SeqCst);
            let base_elapsed = self.elapsed_time.load(Ordering::SeqCst);
            (now - start + base_elapsed) as i64
        } else {
            self.elapsed_time.load(Ordering::SeqCst) as i64
        };
        
        let remaining_seconds = total_seconds - elapsed_seconds;
        
        let work_time_today = if is_running && !is_break {
            let now = Local::now().timestamp() as u64;
            let work_start = self.work_time_start.load(Ordering::SeqCst);
            let current_session = now - work_start;
            self.work_time_today.load(Ordering::SeqCst) + current_session
        } else {
            self.work_time_today.load(Ordering::SeqCst)
        };
        
        let daily_work_seconds = self.daily_work_hours.load(Ordering::SeqCst) * 3600;
        let work_percentage = (work_time_today as f64 / daily_work_seconds as f64) * 100.0;
        
        if remaining_seconds <= 0 {
            if !is_break {
                self.completed_pomodoros.fetch_add(1, Ordering::SeqCst);
            }
            
            if !is_break && is_running {
                let now = Local::now().timestamp() as u64;
                let work_start = self.work_time_start.load(Ordering::SeqCst);
                let work_time = now - work_start;
                self.work_time_today.fetch_add(work_time, Ordering::SeqCst);
            }
            
            self.is_break.store(!is_break, Ordering::SeqCst);
            self.elapsed_time.store(0, Ordering::SeqCst);
            
            if is_running {
                let now = Local::now().timestamp() as u64;
                self.start_time.store(now, Ordering::SeqCst);
                
                if is_break {
                    self.work_time_start.store(now, Ordering::SeqCst);
                }
            }
        }
        
        let work_duration_seconds = self.work_duration.lock().unwrap().num_seconds();
        let break_duration_seconds = self.break_duration.lock().unwrap().num_seconds();
        
        json!({
            "is_running": is_running,
            "is_break": is_break,
            "remaining_seconds": std::cmp::max(0, remaining_seconds),
            "total_seconds": total_seconds,
            "completed_pomodoros": completed_pomodoros,
            "work_time_today": work_time_today,
            "work_percentage": work_percentage,
            "work_duration_seconds": work_duration_seconds,
            "break_duration_seconds": break_duration_seconds,
            "daily_work_hours": self.daily_work_hours.load(Ordering::SeqCst),
        })
    }
}