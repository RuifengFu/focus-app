<template>
  <div class="app-container">
    <header>
      <h1>专注助手</h1>
      <div class="time-message">{{ timeMessage }}</div>
    </header>
    
    <div class="main-content">
      <div class="left-panel">
        <MotivationPanel 
          :quote="quote" 
          :timeStats="timeStats"
          @refreshQuote="getRandomQuote"
        />
      </div>
      
      <div class="right-panel">
        <PomodoroTimer 
          :timerStatus="timerStatus"
          @startTimer="startTimer"
          @pauseTimer="pauseTimer"
          @resetTimer="resetTimer"
          @updateSettings="updateTimerSettings"
        />
        
        <TodoList 
          :todos="todos"
          @addTodo="addTodo"
          @toggleTodo="toggleTodo"
          @deleteTodo="deleteTodo"
        />
      </div>
    </div>
  </div>
</template>

<script>

import { invoke } from '@tauri-apps/api/core';
import { open } from '@tauri-apps/plugin-shell';
import MotivationPanel from './components/MotivationPanel.vue';
import PomodoroTimer from './components/PomodoroTimer.vue';
import TodoList from './components/TodoList.vue';

export default {
  components: {
    MotivationPanel,
    PomodoroTimer,
    TodoList,
  },
  
  data() {
    return {
      todos: [],
      quote: '',
      timeStats: {},
      timerStatus: {
        is_running: false,
        is_break: false,
        remaining_seconds: 1500,
        total_seconds: 1500,
        completed_pomodoros: 0,
      },
      timeMessage: '',
    };
  },
  
  created() {
    this.loadData();
    
    // 定时刷新数据
    setInterval(() => {
      this.refreshTimerStatus();
      this.refreshTimeStats();
    }, 1000);
  },
  
  methods: {
    async loadData() {
      await this.refreshTodoList();
      await this.getRandomQuote();
      await this.refreshTimerStatus();
      await this.refreshTimeStats();
    },
    
    async refreshTodoList() {
      try {
        this.todos = await invoke('get_todos');
      } catch (error) {
        console.error('Error loading todos:', error);
      }
    },
    
    async addTodo(title) {
      try {
        this.todos = await invoke('add_todo', { title });
      } catch (error) {
        console.error('Error adding todo:', error);
      }
    },
    
    async toggleTodo(id) {
      try {
        this.todos = await invoke('toggle_todo', { id });
      } catch (error) {
        console.error('Error toggling todo:', error);
      }
    },
    
    async deleteTodo(id) {
      try {
        this.todos = await invoke('delete_todo', { id });
      } catch (error) {
        console.error('Error deleting todo:', error);
      }
    },
    
    async getRandomQuote() {
      try {
        this.quote = await invoke('get_random_quote');
      } catch (error) {
        console.error('Error getting quote:', error);
      }
    },
    
    async refreshTimeStats() {
      try {
        this.timeStats = await invoke('get_time_spent_stats');
        this.timeMessage = this.timeStats.motivational_message;
      } catch (error) {
        console.error('Error getting time stats:', error);
      }
    },
    
    async refreshTimerStatus() {
      try {
        this.timerStatus = await invoke('get_timer_status');
      } catch (error) {
        console.error('Error getting timer status:', error);
      }
    },
    
    async startTimer() {
      try {
        this.timerStatus = await invoke('start_timer');
      } catch (error) {
        console.error('Error starting timer:', error);
      }
    },
    
    async pauseTimer() {
      try {
        this.timerStatus = await invoke('pause_timer');
      } catch (error) {
        console.error('Error pausing timer:', error);
      }
    },
    
    async resetTimer() {
      try {
        this.timerStatus = await invoke('reset_timer');
      } catch (error) {
        console.error('Error resetting timer:', error);
      }
    },
    
    async updateTimerSettings(settings) {
      try {
        this.timerStatus = await invoke('update_timer_settings', { 
          workTimeMinutes: settings.workTimeMinutes,
          breakTimeMinutes: settings.breakTimeMinutes,
          dailyWorkHours: settings.dailyWorkHours
        });
      } catch (error) {
        console.error('Error updating timer settings:', error);
      }
    },
  },
};
</script>

<style>
.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
}

header {
  text-align: center;
  margin-bottom: 20px;
}

.time-message {
  color: #e74c3c;
  font-weight: bold;
  margin-top: 10px;
  white-space: pre-line;
}

.main-content {
  display: flex;
  gap: 20px;
}

.left-panel, .right-panel {
  flex: 1;
}

@media screen and (max-width: 768px) {
  .main-content {
    flex-direction: column;
  }
}
</style>