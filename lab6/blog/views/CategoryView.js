/**
 * 路由视图：分类
 * 用计算属性按分类聚合文章（对象 + Set 去重），点击分类通过 router.push 编程式导航
 */
const CategoryView = {
  data() {
    return { articles: window.blogArticles };
  },
  computed: {
    categories() {
      const map = {};
      this.articles.forEach(article => {
        map[article.category] = (map[article.category] || 0) + 1;
      });
      return Object.keys(map).map(name => ({ name, count: map[name] }));
    }
  },
  methods: {
    goCategory(name) {
      this.$router.push('/category/' + encodeURIComponent(name));
    }
  },
  template: `
    <div>
      <h2 class="section-title">文章分类</h2>
      <ul class="side-list card-block">
        <li v-for="item in categories" :key="item.name">
          <a href="javascript:void(0)" @click="goCategory(item.name)">{{ item.name }}</a>
          <span>{{ item.count }} 篇</span>
        </li>
      </ul>
      <p style="font-size:13px;color:#8a94a6">提示：点击分类会通过 this.$router.push() 进行编程式跳转。</p>
    </div>
  `
};

/** 分类下的文章列表：/category/:name */
const CategoryDetailView = {
  components: { PostList },
  computed: {
    name() {
      return this.$route.params.name;
    },
    list() {
      return window.blogArticles.filter(article => article.category === this.name);
    }
  },
  template: `
    <div>
      <h2 class="section-title">分类：{{ name }}</h2>
      <post-list :articles="list" :keyword="''"></post-list>
    </div>
  `
};
