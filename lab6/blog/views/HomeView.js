/**
 * 路由视图：首页
 * 搜索框子组件做“输入”，父组件保存关键字并计算 filteredArticles，再通过 props 下发给列表组件
 */
const HomeView = {
  components: { SearchBox, PostList },
  data() {
    return {
      articles: window.blogArticles,
      keyword: '',
      searchFeedback: '尚未输入搜索关键词。'
    };
  },
  computed: {
    filteredArticles() {
      const kw = this.keyword.trim().toLowerCase();
      if (!kw) return this.articles;
      return this.articles.filter(article =>
        article.title.toLowerCase().includes(kw) ||
        article.summary.toLowerCase().includes(kw)
      );
    }
  },
  watch: {
    keyword(newValue, oldValue) {
      if (!newValue) {
        this.searchFeedback = oldValue
          ? `已清空搜索条件，共显示全部 ${this.articles.length} 篇博文。`
          : '尚未输入搜索关键词。';
        return;
      }
      this.searchFeedback = oldValue
        ? `关键字由“${oldValue}”变为“${newValue}”，共找到 ${this.filteredArticles.length} 篇博文。`
        : `开始搜索“${newValue}”，共找到 ${this.filteredArticles.length} 篇博文。`;
    }
  },
  methods: {
    resetSearch() {
      this.keyword = '';
      this.searchFeedback = `已重置，共显示全部 ${this.articles.length} 篇博文。`;
    }
  },
  template: `
    <div>
      <!-- v-model:keyword 是 v-model 的具名写法：:model-value + @update:model-value -->
      <search-box
        v-model:keyword="keyword"
        :feedback="searchFeedback"
        @search="searchFeedback = '点击搜索：' + (keyword || '（空）')">
      </search-box>

      <h2 class="section-title">
        最新博文 <small>共 {{ articles.length }} 篇，当前显示 {{ filteredArticles.length }} 篇</small>
      </h2>

      <post-list :articles="filteredArticles" :keyword="keyword"></post-list>
    </div>
  `
};
