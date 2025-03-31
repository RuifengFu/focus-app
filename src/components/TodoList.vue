<template>
  <div class="todo-list">
    <h2>待办事项</h2>
    
    <div class="add-todo">
      <input 
        v-model="newTodoTitle" 
        type="text" 
        placeholder="添加新任务..." 
        @keyup.enter="submitTodo"
      />
      <button @click="submitTodo">添加</button>
    </div>
    
    <ul class="todos">
      <li v-for="todo in todos" :key="todo.id" class="todo-item" :class="{ 'completed': todo.completed }">
        <div class="todo-content">
          <label class="checkbox">
            <input type="checkbox" :checked="todo.completed" @change="toggleTodo(todo.id)" />
            <span class="checkmark"></span>
          </label>
          <span class="todo-title">{{ todo.title }}</span>
        </div>
        <button class="delete-btn" @click="deleteTodo(todo.id)">×</button>
      </li>
    </ul>
    
    <div v-if="todos.length === 0" class="empty-state">
      没有待办事项，立即添加你的第一个任务！
    </div>
    
    <div v-else class="todo-stats">
      <div class="stat">已完成: {{ completedCount }}</div>
      <div class="stat">未完成: {{ pendingCount }}</div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    todos: {
      type: Array,
      default: () => [],
    },
  },
  
  data() {
    return {
      newTodoTitle: '',
    };
  },
  
  computed: {
    completedCount() {
      return this.todos.filter(todo => todo.completed).length;
    },
    
    pendingCount() {
      return this.todos.filter(todo => !todo.completed).length;
    },
  },
  
  methods: {
    submitTodo() {
      if (this.newTodoTitle.trim()) {
        this.$emit('addTodo', this.newTodoTitle);
        this.newTodoTitle = '';
      }
    },
    
    toggleTodo(id) {
      this.$emit('toggleTodo', id);
    },
    
    deleteTodo(id) {
      this.$emit('deleteTodo', id);
    },
  },
};
</script>

<style scoped>
.todo-list {
  background-color: #f8f9fa;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.add-todo {
  display: flex;
  margin-bottom: 20px;
}

.add-todo input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px 0 0 5px;
  font-size: 1rem;
}

.add-todo button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 0 5px 5px 0;
  cursor: pointer;
  font-weight: bold;
}

.todos {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.todo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 10px;
  background-color: white;
  border-radius: 5px;
  margin-bottom: 10px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: background-color 0.2s;
}

.todo-content {
  display: flex;
  align-items: center;
  flex: 1;
}

.todo-title {
  margin-left: 10px;
  transition: text-decoration 0.2s, color 0.2s;
}

.completed .todo-title {
  text-decoration: line-through;
  color: #999;
}

.delete-btn {
  background-color: transparent;
  border: none;
  color: #e74c3c;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0 5px;
}

.todo-stats {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
  font-size: 0.9rem;
  color: #666;
}

.empty-state {
  text-align: center;
  padding: 20px;
  color: #7f8c8d;
  font-style: italic;
}

/* 自定义复选框样式 */
.checkbox {
  display: block;
  position: relative;
  padding-left: 25px;
  cursor: pointer;
  user-select: none;
}

.checkbox input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  position: absolute;
  top: -2px;
  left: 0;
  height: 18px;
  width: 18px;
  background-color: #eee;
  border-radius: 3px;
}

.checkbox:hover input ~ .checkmark {
  background-color: #ccc;
}

.checkbox input:checked ~ .checkmark {
  background-color: #2196F3;
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

.checkbox input:checked ~ .checkmark:after {
  display: block;
}

.checkbox .checkmark:after {
  left: 6px;
  top: 2px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}
</style>