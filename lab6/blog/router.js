/**
 * 路由配置：地址与组件的对应关系
 * 使用 Hash 模式，双击打开 html 文件也能直接运行
 */
const router = VueRouter.createRouter({
  history: VueRouter.createWebHashHistory(),
  routes: [
    { path: '/', name: 'home', component: HomeView, meta: { title: '首页' } },
    { path: '/category', name: 'category', component: CategoryView, meta: { title: '分类' } },
    { path: '/category/:name', name: 'category-detail', component: CategoryDetailView, meta: { title: '分类' } },
    { path: '/article/:id', name: 'article', component: ArticleView, props: true, meta: { title: '文章' } },
    { path: '/about', name: 'about', component: AboutView, meta: { title: '关于' } },
    { path: '/message', name: 'message', component: MessageView, meta: { title: '留言板' } },
    { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFoundView, meta: { title: '404' } }
  ],
  // 全局后置守卫：根据 meta 修改页面标题
  scrollBehavior() {
    return { top: 0 };
  }
});

router.afterEach(to => {
  document.title = (to.meta.title ? to.meta.title + ' - ' : '') + '我的博客';
});

/**
 * 根组件 App
 */
const App = {
  components: { SiteHeader },
  data() {
    return { year: new Date().getFullYear() };
  },
  template: `
    <div>
      <site-header></site-header>
      <main class="container">
        <!-- 路由出口 -->
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <keep-alive :include="['AboutView']">
              <component :is="Component"></component>
            </keep-alive>
          </transition>
        </router-view>
      </main>
      <footer>© {{ year }} MyBlog · 实验6 组件化 + Vue Router 版</footer>
    </div>
  `
};

Vue.createApp(App).use(router).mount('#app');
