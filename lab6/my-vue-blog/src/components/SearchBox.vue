<script setup>
// 使用 defineModel 定义可双向绑定的 v-model（Vue 3.4+ 语法糖）
const keyword = defineModel({ type: String, default: '' })

defineProps({
  feedback: { type: String, default: '' }
})
const emit = defineEmits(['search'])
</script>

<template>
  <form class="search-bar" @submit.prevent="emit('search', keyword)">
    <input type="text" v-model.trim="keyword" placeholder="输入关键字搜索文章标题，如：Vue">
    <button type="submit">搜索</button>
    <button type="button" class="ghost" @click="keyword = ''">重置</button>
    <p class="feedback">
      {{ feedback }}
      <template v-if="keyword">（当前关键字：<em>{{ keyword }}</em>）</template>
    </p>
  </form>
</template>
