/**
 * 路由视图：关于
 */
const AboutView = {
  data() {
    return {
      skills: ['HTML / CSS', 'JavaScript', 'Vue 3', 'Vue Router'],
      visits: 1
    };
  },
  template: `
    <div class="card-block">
      <h2 class="section-title" style="margin-top:0">关于我</h2>
      <p>你好，我是软件工程专业的一名学生，正在学习《WEB 全栈开发技术》课程。</p>
      <ul class="about-list">
        <li v-for="skill in skills" :key="skill">✅ {{ skill }}</li>
      </ul>
      <p style="font-size:13px;color:#8a94a6">
        本页被激活次数：{{ visits }}（keep-alive 缓存了组件状态，来回切换不会丢失）
      </p>
    </div>
  `,
  activated() {
    this.visits++;
  }
};
