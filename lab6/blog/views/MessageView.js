/**
 * 路由视图：留言板（使用 MessageBoard 子组件）
 */
const MessageView = {
  components: { MessageBoard },
  data() {
    return { count: window.blogInitialMessages.length };
  },
  template: `
    <div>
      <h2 class="section-title" style="margin-top:0">留言板 <small>共 {{ count }} 条留言</small></h2>
      <message-board @change="n => count = n"></message-board>
    </div>
  `
};
