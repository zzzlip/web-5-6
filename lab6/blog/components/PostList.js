/**
 * 子组件：博文列表
 * 接收父组件传入的博文数组，用 v-for 循环渲染 PostCard，无数据时显示空状态
 */
const PostList = {
  components: { PostCard },
  props: {
    articles: {
      type: Array,
      default: () => []
    },
    keyword: {
      type: String,
      default: ''
    }
  },
  template: `
    <div>
      <div class="article-list" v-if="articles.length">
        <post-card
          v-for="article in articles"
          :key="article.id"
          :article="article">
        </post-card>
      </div>
      <p class="empty" v-else>没有找到与“{{ keyword }}”相关的博文，请更换关键字。</p>
    </div>
  `
};
