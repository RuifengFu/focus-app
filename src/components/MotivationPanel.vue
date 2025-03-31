<template>
  <div class="motivation-panel">
    <div class="quote-container">
      <p class="quote">{{ quote }}</p>
      <button class="refresh-btn" @click="$emit('refreshQuote')">刷新</button>
    </div>
    
    <div class="stats-container">
      <h3>时间统计</h3>
      
      <!-- 增强今日时间进度条 -->
      <div class="progress-item">
        <div class="progress-label">
          <span>今日时间</span>
          <span>{{ timeStats.day_percentage?.toFixed(4) }}%</span>
        </div>
        <div class="progress-bar">
          <div class="progress-fill time-flow" 
               :style="{ 
                 width: `${timeStats.day_percentage || 0}%`,
                 backgroundColor: getDayColor(timeStats.day_percentage)
               }">
            <div class="pulse-effect"></div>
          </div>
        </div>
      </div>
      
      <!-- 年度进度条 -->
      <div class="progress-item">
        <div class="progress-label">
          <span>年度进度</span>
          <span>{{ timeStats.year_percentage?.toFixed(4) }}%</span>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" 
               :style="{ 
                 width: `${timeStats.year_percentage || 0}%`,
                 backgroundColor: getYearColor(timeStats.year_percentage)
               }"></div>
        </div>
      </div>
      
      <!-- 生命进度条 -->
      <div class="progress-item">
        <div class="progress-label">
          <span>生命进度</span>
          <span>{{ timeStats.life_percentage?.toFixed(4) }}%</span>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" 
               :style="{ 
                 width: `${timeStats.life_percentage || 0}%`, 
                 backgroundColor: '#e74c3c' 
               }"></div>
        </div>
      </div>
      
      <div class="stats-detail">
        <p>剩余工作日: <strong>{{ timeStats.remaining_work_days?.toLocaleString() }}</strong> 天</p>
        <p>今年已过: <strong>{{ timeStats.day_of_year }}/{{ timeStats.days_in_year }}</strong> 天</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    quote: {
      type: String,
      default: ''
    },
    timeStats: {
      type: Object,
      default: () => ({})
    }
  },
  methods: {
    // 根据时间百分比返回颜色，从绿色过渡到红色
    getDayColor(percentage) {
      if (!percentage) return '#3498db';
      // 下午开始变色
      if (percentage <= 50) return '#2ecc71'; // 绿色
      if (percentage <= 75) return '#f39c12'; // 橙色
      return '#e74c3c'; // 红色
    },
    // 年度进度颜色
    getYearColor(percentage) {
      if (!percentage) return '#3498db';
      if (percentage <= 25) return '#2ecc71'; // 绿色
      if (percentage <= 50) return '#3498db'; // 蓝色
      if (percentage <= 75) return '#f39c12'; // 橙色
      return '#e74c3c'; // 红色
    }
  }
}
</script>

<style scoped>
.motivation-panel {
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.quote-container {
  margin-bottom: 20px;
  position: relative;
}

.quote {
  font-style: italic;
  font-size: 1.1rem;
  line-height: 1.6;
  color: #333;
}

.refresh-btn {
  position: absolute;
  top: 0;
  right: 0;
  background: transparent;
  border: none;
  color: #3498db;
  cursor: pointer;
}

.stats-container {
  border-top: 1px solid #ddd;
  padding-top: 15px;
}

.progress-item {
  margin-bottom: 15px;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-size: 0.9rem;
}

.progress-bar {
  height: 12px; /* 增加高度 */
  background-color: #eee;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
}

.progress-fill {
  height: 100%;
  background-color: #3498db;
  border-radius: 6px;
  transition: width 1s ease, background-color 1s ease;
  position: relative;
}

/* 增加时间流逝感的样式 */
.time-flow {
  background-image: linear-gradient(
    45deg,
    rgba(255, 255, 255, 0.15) 25%,
    transparent 25%,
    transparent 50%,
    rgba(255, 255, 255, 0.15) 50%,
    rgba(255, 255, 255, 0.15) 75%,
    transparent 75%,
    transparent
  );
  background-size: 20px 20px;
  animation: progress-bar-stripes 1s linear infinite;
}

@keyframes progress-bar-stripes {
  from { background-position: 20px 0; }
  to { background-position: 0 0; }
}

/* 添加脉冲效果 */
.pulse-effect {
  position: absolute;
  right: 0;
  top: 0;
  height: 100%;
  width: 4px;
  background-color: rgba(255,255,255,0.8);
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.2; }
  100% { opacity: 1; }
}

.stats-detail {
  margin-top: 20px;
  font-size: 0.9rem;
  color: #666;
}

.stats-detail p {
  margin: 5px 0;
}
</style>