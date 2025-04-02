#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

mod todo;
mod timer;
mod quotes;

use todo::{Todo, TodoList};
use timer::PomodoroTimer;
use quotes::QuotesManager;
use std::sync::Mutex;
use tauri::State;

struct AppState {
    todo_list: Mutex<TodoList>,
    timer: Mutex<PomodoroTimer>,
    quotes: Mutex<QuotesManager>,
}

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .manage(AppState {
            todo_list: Mutex::new(TodoList::new()),
            timer: Mutex::new(PomodoroTimer::new()),
            quotes: Mutex::new(QuotesManager::new()),
        })
        .invoke_handler(tauri::generate_handler![
            get_todos,
            add_todo,
            toggle_todo,
            delete_todo,
            start_timer,
            pause_timer,
            reset_timer,
            skip_timer,
            toggle_sound,
            update_timer_settings,
            get_timer_status,
            get_random_quote,
            get_time_spent_stats
        ])
        .run(tauri::generate_context!("tauri.conf.json"))
        .expect("error while running tauri application");
}

#[tauri::command]
fn get_todos(state: State<AppState>) -> Vec<Todo> {
    state.todo_list.lock().unwrap().get_all()
}

#[tauri::command]
fn add_todo(state: State<AppState>, title: String) -> Vec<Todo> {
    state.todo_list.lock().unwrap().add(title);
    state.todo_list.lock().unwrap().get_all()
}

#[tauri::command]
fn toggle_todo(state: State<AppState>, id: u32) -> Vec<Todo> {
    state.todo_list.lock().unwrap().toggle(id);
    state.todo_list.lock().unwrap().get_all()
}

#[tauri::command]
fn delete_todo(state: State<AppState>, id: u32) -> Vec<Todo> {
    state.todo_list.lock().unwrap().delete(id);
    state.todo_list.lock().unwrap().get_all()
}

#[tauri::command]
fn start_timer(state: State<AppState>) -> serde_json::Value {
    state.timer.lock().unwrap().start()
}

#[tauri::command]
fn pause_timer(state: State<AppState>) -> serde_json::Value {
    state.timer.lock().unwrap().pause()
}

#[tauri::command]
fn reset_timer(state: State<AppState>) -> serde_json::Value {
    state.timer.lock().unwrap().reset()
}

#[tauri::command]
fn get_timer_status(state: State<AppState>) -> serde_json::Value {
    state.timer.lock().unwrap().get_status()
}

#[tauri::command]
fn get_random_quote(state: State<AppState>) -> String {
    state.quotes.lock().unwrap().get_random_quote()
}

#[tauri::command]
fn get_time_spent_stats(state: State<AppState>) -> serde_json::Value {
    state.quotes.lock().unwrap().get_time_spent_stats()
}

#[tauri::command]
fn update_timer_settings(state: State<AppState>, work_time_minutes: u64, break_time_minutes: u64, daily_work_hours: u64) -> serde_json::Value {
    state.timer.lock().unwrap().update_settings(work_time_minutes, break_time_minutes, daily_work_hours)
}

#[tauri::command]
fn skip_timer(state: State<AppState>) -> serde_json::Value {
    state.timer.lock().unwrap().skip_current()
}

#[tauri::command]
fn toggle_sound(state: State<AppState>, enabled: bool) -> serde_json::Value {
    state.timer.lock().unwrap().toggle_sound(enabled)
}