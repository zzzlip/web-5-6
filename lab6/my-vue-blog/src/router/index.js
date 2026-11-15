import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

// 路由懒加载：除首页外，其余页面在访问时才下载对应代码块
const routes = [
  { path: '/', name: 'home', component: HomeView, meta: { title: '首页' } },
  { path: '/about', name: 'about', component: () => import('../views/AboutView.vue'), meta: { title: '关于' } },
  { path: '/message', name: 'message', component: () => import('../views/MessageView.vue'), meta: { title: '留言板' } },
  { path: '/article/:id', name: 'article', component: () => import('../views/ArticleView.vue'), props: true, meta: { title: '文章详情' } },
  { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('../views/NotFoundView.vue'), meta: { title: '404' } }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

router.afterEach((to) => {
  document.title = (to.meta.title ? to.meta.title + ' - ' : '') + '我的博客'
})

export default router
