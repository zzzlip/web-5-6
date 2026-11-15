/**
 * 路由视图：文章详情
 * 动态路由参数 id 来自 $route.params，通过计算属性从全部数据中查找对应文章
 */
const ArticleView = {
  computed: {
    article() {
      const id = Number(this.$route.params.id);
      return window.blogArticles.find(item => item.id === id);
    }
  },
  template: `
    <div class="article-detail card-block" v-if="article">
      <h2>{{ article.title }}</h2>
      <p class="meta">
        作者：{{ article.author }} · {{ article.date }} ·
        <span class="badge">{{ article.category }}</span> · 阅读 {{ article.likes * 13 }}
      </p>
      <div class="content">
        <p>{{ article.summary }}</p>
        <p>（正文略）本页通过路由参数 <b>$route.params.id = {{ $route.params.id }}</b> 找到对应文章并渲染。</p>
      </div>
      <router-link class="back" to="/">← 返回首页</router-link>
    </div>
    <p class="empty" v-else>文章不存在，<router-link to="/">返回首页</router-link></p>
  `
};
