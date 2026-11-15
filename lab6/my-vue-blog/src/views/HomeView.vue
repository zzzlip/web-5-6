<script setup>
import { computed, ref, watch } from 'vue'
import SearchBox from '../components/SearchBox.vue'
import PostList from '../components/PostList.vue'
import { articles } from '../data/posts'

const keyword = ref('')
const searchFeedback = ref('尚未输入搜索关键词。')

const filteredArticles = computed(() => {
  const kw = keyword.value.trim().toLowerCase()
  if (!kw) return articles
  return articles.filter(
    (item) => item.title.toLowerCase().includes(kw) || item.summary.toLowerCase().includes(kw)
  )
})

watch(keyword, (newValue) => {
  searchFeedback.value = newValue
    ? `当前关键字“${newValue}”，共找到 ${filteredArticles.value.length} 篇博文。`
    : `已清空搜索条件，共显示全部 ${articles.length} 篇博文。`
})
</script>

<template>
  <div>
    <search-box v-model="keyword" :feedback="searchFeedback" />
    <h2 class="section-title">
      最新博文 <small>共 {{ articles.length }} 篇，当前显示 {{ filteredArticles.length }} 篇</small>
    </h2>
    <post-list :articles="filteredArticles" :keyword="keyword" />
  </div>
</template>
