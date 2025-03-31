use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use chrono::{Local, TimeZone};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Todo {
    pub id: u32,
    pub title: String,
    pub completed: bool,
    pub created_at: i64,
}

pub struct TodoList {
    todos: HashMap<u32, Todo>,
    next_id: u32,
}

impl TodoList {
    pub fn new() -> Self {
        Self {
            todos: HashMap::new(),
            next_id: 1,
        }
    }
    
    pub fn add(&mut self, title: String) {
        let now = Local::now().timestamp();
        let todo = Todo {
            id: self.next_id,
            title,
            completed: false,
            created_at: now,
        };
        
        self.todos.insert(self.next_id, todo);
        self.next_id += 1;
    }
    
    pub fn toggle(&mut self, id: u32) {
        if let Some(todo) = self.todos.get_mut(&id) {
            todo.completed = !todo.completed;
        }
    }
    
    pub fn delete(&mut self, id: u32) {
        self.todos.remove(&id);
    }
    
    pub fn get_all(&self) -> Vec<Todo> {
        let mut todos: Vec<Todo> = self.todos.values().cloned().collect();
        todos.sort_by(|a, b| b.created_at.cmp(&a.created_at));
        todos
    }
    
    pub fn get_completed_count(&self) -> usize {
        self.todos.values().filter(|todo| todo.completed).count()
    }
    
    pub fn get_pending_count(&self) -> usize {
        self.todos.values().filter(|todo| !todo.completed).count()
    }
}