<template>
  <div class="pomodoro-timer">
    <h3>番茄计时器</h3>
    
    <div class="settings-panel">
      <div class="setting-item">
        <label>工作时间 (分钟)</label>
        <div class="setting-controls">
          <button @click="decreaseWorkTime" :disabled="workTimeMinutes <= 5">-</button>
          <span>{{ workTimeMinutes }}</span>
          <button @click="increaseWorkTime" :disabled="workTimeMinutes >= 60">+</button>
        </div>
      </div>
      
      <div class="setting-item">
        <label>休息时间 (分钟)</label>
        <div class="setting-controls">
          <button @click="decreaseBreakTime" :disabled="breakTimeMinutes <= 1">-</button>
          <span>{{ breakTimeMinutes }}</span>
          <button @click="increaseBreakTime" :disabled="breakTimeMinutes >= 30">+</button>
        </div>
      </div>
      
      <div class="setting-item">
        <label>每日工作时间 (小时)</label>
        <div class="setting-controls">
          <button @click="decreaseDailyWorkHours" :disabled="dailyWorkHours <= 1">-</button>
          <span>{{ dailyWorkHours }}</span>
          <button @click="increaseDailyWorkHours" :disabled="dailyWorkHours >= 12">+</button>
        </div>
      </div>
    </div>
    
    <div class="timer-display">
      <span class="time">{{ formatTime(timerStatus.remaining_seconds) }}</span>
      <span class="mode">{{ timerStatus.is_break ? '休息时间' : '工作时间' }}</span>
    </div>
    
    <div class="timer-progress">
      <div class="progress-bar">
        <div 
          class="progress-fill animated" 
          :style="{ 
            width: `${getTimerPercentage()}%`,
            backgroundColor: getTimerColor()
          }"
        >
          <div class="ticker" v-if="timerStatus.is_running"></div>
        </div>
      </div>
    </div>
    
    <!-- 添加今日工作时间进度条 -->
    <div class="work-progress">
      <div class="progress-label">
        <span>今日工作时间</span>
        <span>{{ (timerStatus.work_percentage || 0).toFixed(2) }}%</span>
      </div>
      <div class="progress-bar">
        <div 
          class="progress-fill work-flow" 
          :style="{ 
            width: `${timerStatus.work_percentage || 0}%`,
            backgroundSize: timerStatus.is_running && !timerStatus.is_break ? '15px 15px' : '0 0'
          }"
        ></div>
      </div>
      <div class="work-time">
        {{ formatWorkTime(timerStatus.work_time_today || 0) }} / {{ dailyWorkHours }}小时
      </div>
    </div>
    
    <div class="timer-controls">
      <button @click="toggleTimer" :disabled="timerStatus.remaining_seconds <= 0"
              :class="{ 'active': timerStatus.is_running }">
        {{ timerStatus.is_running ? '暂停' : '开始' }}
      </button>
      <button @click="resetTimer">重置</button>
      <button @click="applySettings" :disabled="!settingsChanged">应用设置</button>
    </div>
    
    <div class="pomodoro-count">
      已完成番茄: {{ timerStatus.completed_pomodoros }}
    </div>
  </div>
</template>

<script>
export default {
  props: {
    timerStatus: {
      type: Object,
      required: true
    }
  },
  
  data() {
    return {
      // 设置选项
      workTimeMinutes: 25,
      breakTimeMinutes: 5,
      dailyWorkHours: 8,
      // 原始设置，用于检测变化
      originalSettings: {
        workTimeMinutes: 25,
        breakTimeMinutes: 5,
        dailyWorkHours: 8
      }
    };
  },
  
  computed: {
    settingsChanged() {
      return this.workTimeMinutes !== this.originalSettings.workTimeMinutes ||
             this.breakTimeMinutes !== this.originalSettings.breakTimeMinutes ||
             this.dailyWorkHours !== this.originalSettings.dailyWorkHours;
    }
  },
  
  created() {
    // 从计时器状态初始化设置
    if (this.timerStatus) {
      this.workTimeMinutes = Math.floor(this.timerStatus.work_duration_seconds / 60) || 25;
      this.breakTimeMinutes = Math.floor(this.timerStatus.break_duration_seconds / 60) || 5;
      this.dailyWorkHours = this.timerStatus.daily_work_hours || 8;
      
      // 更新原始设置
      this.originalSettings = {
        workTimeMinutes: this.workTimeMinutes,
        breakTimeMinutes: this.breakTimeMinutes,
        dailyWorkHours: this.dailyWorkHours
      };
    }
  },
  
  methods: {
    formatTime(seconds) {
      const mins = Math.floor(seconds / 60);
      const secs = seconds % 60;
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    },
    
    formatWorkTime(seconds) {
      const hours = Math.floor(seconds / 3600);
      const mins = Math.floor((seconds % 3600) / 60);
      return `${hours}小时${mins}分钟`;
    },
    
    toggleTimer() {
      if (this.timerStatus.is_running) {
        this.$emit('pauseTimer');
      } else {
        this.$emit('startTimer');
      }
    },
    
    resetTimer() {
      this.$emit('resetTimer');
    },
    
    getTimerPercentage() {
      if (!this.timerStatus.total_seconds) return 0;
      return ((this.timerStatus.total_seconds - this.timerStatus.remaining_seconds) / this.timerStatus.total_seconds) * 100;
    },
    
    getTimerColor() {
      if (this.timerStatus.is_break) {
        return '#27ae60'; // 休息时间为绿色
      }
      
      // 工作时间颜色渐变
      const percentage = this.getTimerPercentage();
      if (percentage < 33) return '#3498db'; // 蓝色
      if (percentage < 66) return '#f39c12'; // 橙色
      return '#e74c3c'; // 红色
    },
    
    // 工作时间设置
    increaseWorkTime() {
      this.workTimeMinutes = Math.min(60, this.workTimeMinutes + 5);
    },
    
    decreaseWorkTime() {
      this.workTimeMinutes = Math.max(5, this.workTimeMinutes - 5);
    },
    
    // 休息时间设置
    increaseBreakTime() {
      this.breakTimeMinutes = Math.min(30, this.breakTimeMinutes + 1);
    },
    
    decreaseBreakTime() {
      this.breakTimeMinutes = Math.max(1, this.breakTimeMinutes - 1);
    },
    
    // 每日工作时间设置
    increaseDailyWorkHours() {
      this.dailyWorkHours = Math.min(12, this.dailyWorkHours + 1);
    },
    
    decreaseDailyWorkHours() {
      this.dailyWorkHours = Math.max(1, this.dailyWorkHours - 1);
    },
    
    // 应用设置
    applySettings() {
      this.$emit('updateSettings', {
        workTimeMinutes: this.workTimeMinutes,
        breakTimeMinutes: this.breakTimeMinutes,
        dailyWorkHours: this.dailyWorkHours
      });
      
      // 更新原始设置，以便重置"设置已更改"标志
      this.originalSettings = {
        workTimeMinutes: this.workTimeMinutes,
        breakTimeMinutes: this.breakTimeMinutes,
        dailyWorkHours: this.dailyWorkHours
      };
    }
  }
}
</script>

<style scoped>
.pomodoro-timer {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.settings-panel {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.setting-item {
  flex: 1;
  min-width: 120px;
}

.setting-item label {
  display: block;
  margin-bottom: 5px;
  font-size: 0.85rem;
  color: #666;
}

.setting-controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 100px;
}

.setting-controls button {
  width: 30px;
  height: 30px;
  border: 1px solid #ddd;
  background-color: #f5f5f5;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.setting-controls button:hover:not(:disabled) {
  background-color: #e5e5e5;
}

.setting-controls button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.timer-display {
  text-align: center;
  margin-bottom: 15px;
}

.time {
  font-size: 3rem;
  font-weight: bold;
  font-family: monospace;
  color: #333;
  display: block;
}

.mode {
  font-size: 1rem;
  color: #666;
}

.timer-progress, .work-progress {
  margin-bottom: 20px;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-size: 0.9rem;
}

.progress-bar {
  height: 12px;
  background-color: #eee;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
}

.progress-fill {
  height: 100%;
  background-color: #3498db;
  border-radius: 6px;
  transition: width 1s linear, background-color 1s ease;
  position: relative;
}

/* 动画效果 */
.animated {
  transition: width 1s linear, background-color 1s ease;
}

/* 添加时钟滴答效果 */
.ticker {
  position: absolute;
  right: 0;
  top: 0;
  height: 100%;
  width: 3px;
  background-color: rgba(255,255,255,0.8);
  animation: tick 1s linear infinite;
}

@keyframes tick {
  0% { opacity: 1; }
  50% { opacity: 0.2; }
  100% { opacity: 1; }
}

/* 工作流动效果 */
.work-flow {
  background-image: linear-gradient(
    -45deg,
    rgba(255, 255, 255, 0.2) 25%,
    transparent 25%,
    transparent 50%,
    rgba(255, 255, 255, 0.2) 50%,
    rgba(255, 255, 255, 0.2) 75%,
    transparent 75%,
    transparent
  );
  animation: work-flow 1.5s linear infinite;
}

@keyframes work-flow {
  from { background-position: 0 0; }
  to { background-position: 15px 0; }
}

.work-time {
  text-align: center;
  font-size: 0.9rem;
  color: #666;
  margin-top: 5px;
}

.timer-controls {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 15px;
}

.timer-controls button {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  background-color: #3498db;
  color: white;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
}

.timer-controls button:hover:not(:disabled) {
  background-color: #2980b9;
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.timer-controls button:active, .timer-controls button.active {
  background-color: #2980b9;
  transform: translateY(0);
}

.timer-controls button:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.pomodoro-count {
  text-align: center;
  font-size: 0.9rem;
  color: #666;
}
</style>