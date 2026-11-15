<script setup>
const skills = ['HTML / CSS', 'JavaScript', 'Vue 3 + Vite', 'Vue Router']
</script>

<template>
  <div class="card-block">
    <h2 class="section-title" style="margin-top: 0">关于我</h2>
    <p>你好，我是软件工程专业的一名学生，正在学习《WEB 全栈开发技术》课程。</p>
    <ul>
      <li v-for="skill in skills" :key="skill">✅ {{ skill }}</li>
    </ul>
  </div>
</template>
