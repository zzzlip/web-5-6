<script setup>
import { ref } from 'vue'
import SiteHeader from './components/SiteHeader.vue'

const year = ref(new Date().getFullYear())
</script>

<template>
  <SiteHeader title="MyBlog · 我的博客（Vite 版）" />
  <main class="container">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </main>
  <footer>© {{ year }} MyBlog · 实验6 拓展：Vite + Vue 3 工程化</footer>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.18s ease, transform 0.18s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(6px);
}
</style>
