/**
 * 子组件：留言板
 * 自己维护留言数据；父组件可通过绑定 :count 读取数量（本例用 emit 通知）
 */
const MessageBoard = {
  data() {
    return {
      messages: window.blogInitialMessages,
      newNickname: '',
      newContent: ''
    };
  },
  emits: ['change'],
  template: `
    <section class="message-board">
      <form class="message-form" @submit.prevent="addMessage">
        <input class="nickname" type="text" ref="nicknameInput" v-model.trim="newNickname" placeholder="昵称" maxlength="10">
        <input class="content" type="text" ref="contentInput" v-model.trim="newContent" placeholder="说点什么吧，回车键发送">
        <button type="submit" :disabled="!newContent">发表</button>
      </form>

      <p class="empty" v-if="!messages.length">还没有留言，快来抢沙发～</p>
      <ul class="message-list" v-else>
        <li v-for="item in messages" :key="item.id">
          <span class="who" :title="item.nickname">{{ item.nickname }}</span>
          <span class="text">{{ item.content }}</span>
          <span class="time">{{ item.time }}</span>
          <button type="button" class="del" @click="deleteMessage(item.id)">删除</button>
        </li>
      </ul>
    </section>
  `,
  methods: {
    addMessage() {
      const content = this.newContent.trim();
      if (!content) return;
      const now = new Date();
      const pad = n => String(n).padStart(2, '0');
      this.messages.unshift({
        id: Date.now(),
        nickname: this.newNickname || '匿名用户',
        content,
        time: `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())} ${pad(now.getHours())}:${pad(now.getMinutes())}`
      });
      this.newContent = '';
      this.$refs.nicknameInput.focus();
      this.$emit('change', this.messages.length);
    },
    deleteMessage(id) {
      this.messages = this.messages.filter(item => item.id !== id);
      this.$emit('change', this.messages.length);
    }
  }
};
