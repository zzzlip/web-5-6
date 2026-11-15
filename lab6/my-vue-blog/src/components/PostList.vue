<script setup>
import PostCard from './PostCard.vue'

defineProps({
  articles: { type: Array, default: () => [] },
  keyword: { type: String, default: '' }
})
</script>

<template>
  <div class="article-list" v-if="articles.length">
    <PostCard v-for="article in articles" :key="article.id" :article="article" />
  </div>
  <p class="empty" v-else>没有找到与“{{ keyword }}”相关的博文，请更换关键字。</p>
</template>
