<script setup>
// 顶部导航：父组件通过自定义属性 title 传值（defineProps 声明）
defineProps({
  title: { type: String, default: 'MyBlog' }
})
</script>

<template>
  <header>
    <div class="logo">{{ title }}</div>
    <nav class="nav-links">
      <router-link to="/">首页</router-link>
      <router-link to="/about">关于</router-link>
      <router-link to="/message">留言板</router-link>
    </nav>
  </header>
</template>
