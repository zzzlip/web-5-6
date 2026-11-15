/**
 * 子组件：博文卡片
 * 父组件通过 :article 传入博文对象，子组件只负责展示，不直接修改 props
 */
const PostCard = {
  // 对象形式声明 props：可规定类型、是否必传、默认值
  props: {
    article: {
      type: Object,   // 传入的 article 应当是对象
      required: true  // 父组件必须传入
    }
  },
  template: `
    <article class="article">
      <div class="cover" :style="{ background: article.cover }"></div>
      <div class="body">
        <h3>
          <router-link :to="'/article/' + article.id" :title="'阅读全文：' + article.title">
            {{ article.title }}
          </router-link>
        </h3>
        <p class="summary">{{ article.summary }}</p>
        <p class="meta">
          <span>作者：{{ article.author }}</span>
          <span>日期：{{ article.date }}</span>
          <span class="badge">{{ article.category }}</span>
          <span>评论 {{ article.comments }}</span>
          <span>点赞 {{ article.likes }}</span>
        </p>
      </div>
    </article>
  `
};
