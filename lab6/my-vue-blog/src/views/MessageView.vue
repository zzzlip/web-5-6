<script setup>
import { ref } from 'vue'
import { initialMessages } from '../data/posts'

const messages = ref([...initialMessages])
const nickname = ref('')
const content = ref('')

function addMessage() {
  if (!content.value) return
  const now = new Date()
  const pad = (n) => String(n).padStart(2, '0')
  messages.value.unshift({
    id: Date.now(),
    nickname: nickname.value || '匿名用户',
    content: content.value,
    time: `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())} ${pad(now.getHours())}:${pad(now.getMinutes())}`
  })
  content.value = ''
}

function removeMessage(id) {
  messages.value = messages.value.filter((item) => item.id !== id)
}
</script>

<template>
  <div>
    <h2 class="section-title" style="margin-top: 0">留言板 <small>共 {{ messages.length }} 条留言</small></h2>
    <section class="message-board">
      <form class="message-form" @submit.prevent="addMessage">
        <input class="nickname" v-model.trim="nickname" maxlength="10" placeholder="昵称">
        <input class="content" v-model.trim="content" placeholder="说点什么吧，回车键发送">
        <button type="submit" :disabled="!content">发表</button>
      </form>
      <ul class="message-list">
        <li v-for="item in messages" :key="item.id">
          <span class="who">{{ item.nickname }}</span>
          <span class="text">{{ item.content }}</span>
          <span class="time">{{ item.time }}</span>
          <button type="button" class="del" @click="removeMessage(item.id)">删除</button>
        </li>
      </ul>
    </section>
  </div>
</template>
