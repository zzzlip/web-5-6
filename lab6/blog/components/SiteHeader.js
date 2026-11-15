/**
 * 子组件：顶部导航
 * 使用 router-link 进行声明式导航，父组件可通过 :title 自定义站点名称
 */
const SiteHeader = {
  props: {
    title: { type: String, default: 'MyBlog · 我的博客' }
  },
  template: `
    <header>
      <div class="logo">{{ title }}</div>
      <nav class="nav-links">
        <router-link to="/">首页</router-link>
        <router-link to="/category">分类</router-link>
        <router-link to="/about">关于</router-link>
        <router-link to="/message">留言板</router-link>
      </nav>
    </header>
  `
};
