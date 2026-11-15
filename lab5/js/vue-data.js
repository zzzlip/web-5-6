/**
 * 实验5 模拟数据：博客文章 + 初始留言
 * 单独存放为 js 文件，通过 <script> 引入后挂到 window 上，供 Vue 实例的 data 使用
 */
const blogArticles = [
  {
    id: 1,
    title: 'Vue 3 组合式 API 与选项式 API 的区别',
    author: '张三',
    date: '2026-10-08',
    category: '前端开发',
    comments: 12,
    likes: 36,
    cover: 'linear-gradient(135deg,#42b883,#347474)',
    summary: '选项式 API 以 data、methods、computed 等选项组织代码，组合式 API 用 setup 把相关逻辑聚合在一起，本文通过同一个计数器案例对比两种写法。'
  },
  {
    id: 2,
    title: '从 DOM 操作到数据驱动：我理解的 MVVM',
    author: '李四',
    date: '2026-10-15',
    category: '学习笔记',
    comments: 8,
    likes: 25,
    cover: 'linear-gradient(135deg,#5b8def,#3b5bdb)',
    summary: '以前写原生 JS 时到处 getElementById，改成 Vue 后只需要修改数据，视图会自动更新。本文用一个待办列表梳理 MVVM 的双向绑定流程。'
  },
  {
    id: 3,
    title: 'CSS Grid 与 Flex 布局实战总结',
    author: '王五',
    date: '2026-10-22',
    category: 'CSS',
    comments: 15,
    likes: 41,
    cover: 'linear-gradient(135deg,#f0932b,#e17055)',
    summary: '一维排版优先 Flex，二维网格优先 Grid。本文结合博客首页的卡片列表，给出两套布局方案以及常见的 1px 边框、居中问题。'
  },
  {
    id: 4,
    title: '使用 Vue Router 实现单页应用路由',
    author: '赵六',
    date: '2026-10-29',
    category: '前端开发',
    comments: 6,
    likes: 19,
    cover: 'linear-gradient(135deg,#8e44ad,#5f27cd)',
    summary: '单页应用的页面切换本质上是组件的切换。本文介绍 hash 模式与 history 模式的区别，以及 router-link、router-view 的基本用法。'
  }
];

const blogInitialMessages = [
  { id: 1, nickname: '路人甲', content: '写得很清楚，学到了！', time: '2026-10-30 09:12' },
  { id: 2, nickname: '前端小白', content: '请问下一篇能讲讲组件传值吗？', time: '2026-11-02 20:45' }
];
