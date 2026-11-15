<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { articles } from '../data/posts'

const route = useRoute()
const article = computed(() => articles.find((item) => item.id === Number(route.params.id)))
</script>

<template>
  <div class="card-block">
    <div v-if="article" class="article-detail">
      <h2>{{ article.title }}</h2>
      <p class="meta">作者：{{ article.author }} · {{ article.date }} · {{ article.category }}</p>
      <p>{{ article.summary }}</p>
      <router-link to="/">← 返回首页</router-link>
    </div>
    <p v-else class="empty">文章不存在，<router-link to="/">返回首页</router-link></p>
  </div>
</template>
