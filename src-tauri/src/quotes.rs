use rand::seq::SliceRandom;
use rand::thread_rng;
use serde::{Deserialize, Serialize};
use serde_json::json;
use chrono::{Local, Datelike, Timelike};

#[derive(Deserialize, Serialize, Clone)]
pub struct Quote {
    text: String,
    author: String,
}

struct TimeStats {
    start_date: chrono::DateTime<Local>,
    work_days_in_year: u32,
    average_life_expectancy: u32,
}

pub struct QuotesManager {
    quotes: Vec<Quote>,
    stats: TimeStats,
}

impl QuotesManager {
    pub fn new() -> Self {
        // 直接使用 include_str! 宏嵌入 JSON 文件内容
        let quotes_json = include_str!("../resources/quotes.json");
        
        // 解析 JSON
        let quotes: Vec<Quote> = serde_json::from_str(quotes_json).unwrap_or_else(|e| {
            eprintln!("警告: 解析引用文件时出错: {}", e);
            vec![
                Quote {
                    text: "行动是治愈恐惧的良药。".to_string(),
                    author: "佚名".to_string(),
                }
            ]
        });
        
        Self {
            quotes,
            stats: TimeStats {
                start_date: Local::now(),
                work_days_in_year: 250,
                average_life_expectancy: 80,
            },
        }
    }
    
    pub fn get_random_quote(&self) -> String {
        let mut rng = thread_rng();
        if let Some(quote) = self.quotes.choose(&mut rng) {
            format!("\"{}\" —— {}", quote.text, quote.author)
        } else {
            "行动是治愈恐惧的良药。".to_string()
        }
    }
    
    pub fn get_time_spent_stats(&self) -> serde_json::Value {
        let now = Local::now();
        
        // 计算年龄相关信息
        let birth_year = now.year() - 25; // 假设用户25岁，可以在实际应用中获取
        let age = now.year() - birth_year;
        let life_percentage = (age as f64 / self.stats.average_life_expectancy as f64) * 100.0;
        
        // 计算当前年度的工作日信息
        let days_in_year = if now.year() % 4 == 0 && (now.year() % 100 != 0 || now.year() % 400 == 0) {
            366
        } else {
            365
        };
        let day_of_year = now.ordinal();
        let year_percentage = (day_of_year as f64 / days_in_year as f64) * 100.0;
        
        // 计算剩余工作日
        let remaining_work_days = (self.stats.average_life_expectancy as i32 - age as i32) 
                                * self.stats.work_days_in_year as i32;
        
        // 计算今日已流逝时间
        let seconds_in_day = 24 * 60 * 60;
        let seconds_passed = now.hour() * 3600 + now.minute() * 60 + now.second();
        let day_percentage = (seconds_passed as f64 / seconds_in_day as f64) * 100.0;
        
        json!({
            "age": age,
            "life_percentage": life_percentage,
            "year_percentage": year_percentage,
            "day_percentage": day_percentage,
            "remaining_work_days": remaining_work_days,
            "day_of_year": day_of_year,
            "days_in_year": days_in_year,
            "motivational_message": self.get_motivational_message(day_percentage, life_percentage),
        })
    }
    
    fn get_motivational_message(&self, day_percentage: f64, life_percentage: f64) -> String {
        let day_messages = [
            "今天的时间已经过去了{:.3}%，你完成计划了吗？",
            "日光易逝，已经过去了{:.3}%，抓紧时间！",
            "今天{:.3}%的时间已经消逝，永不回来。",
        ];
        
        let life_messages = [
            "你的生命已经消耗了{:.3}%，剩下的时间你打算如何度过？",
            "人生有限，你已经用掉了{:.3}%，不要蹉跎岁月！",
            "生命的{:.3}%已成为过去，让剩下的时间更有意义！",
        ];
        
        let mut rng = thread_rng();
        let day_msg = day_messages.choose(&mut rng).unwrap_or(&day_messages[0]);
        let life_msg = life_messages.choose(&mut rng).unwrap_or(&life_messages[0]);
        
        format!("{}\n{}", 
            day_msg.replace("{:.3}", &format!("{:.3}", day_percentage)),
            life_msg.replace("{:.3}", &format!("{:.3}", life_percentage))
        )
    }
}