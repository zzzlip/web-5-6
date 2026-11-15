<script setup>
// 子组件：博文卡片，只负责展示
defineProps({
  article: {
    type: Object,
    required: true
  }
})
</script>

<template>
  <article class="article">
    <div class="cover" :style="{ background: article.cover }"></div>
    <div class="body">
      <h3>
        <router-link :to="`/article/${article.id}`" :title="`阅读全文：${article.title}`">
          {{ article.title }}
        </router-link>
      </h3>
      <p class="summary">{{ article.summary }}</p>
      <p class="meta">
        <span>作者：{{ article.author }}</span>
        <span>日期：{{ article.date }}</span>
        <span class="badge">{{ article.category }}</span>
        <span>评论 {{ article.comments }}</span>
        <span>点赞 {{ article.likes }}</span>
      </p>
    </div>
  </article>
</template>
