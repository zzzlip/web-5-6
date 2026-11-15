import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'

// 创建应用 -> 安装路由 -> 挂载
createApp(App).use(router).mount('#app')
