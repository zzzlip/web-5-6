# 实验5-6：Vue.js 基本语法、常用指令与组件、路由

前端代码仓库，直接用浏览器打开 html 文件即可运行（Vue 3.5.44、Vue Router 4.6.3 已放在本地 `js/` 目录，无需联网）。

## 目录

```
lab5/                            实验5：Vue.js 基本语法和常用指令
  index.html                     常用指令综合练习（选项式 API、v-html/v-bind/v-if/v-for/v-on/v-model/v-text/v-show、computed/watch）
  blog.html                      用 Vue 重构实验4的博客主页（博文列表 / 标题搜索 / 留言板）
  todo.html                      选做：待办事项 TodoList（完成状态、编辑、分类统计）
  css/blog.css                   博客样式
  js/vue-data.js                 模拟数据
  js/vue.global.js               Vue 3 本地文件

lab6/                            实验6：组件和路由基础
  demo/01-options-api.html       选项式 API 基本结构
  demo/02-local-component.html   局部组件的定义、注册、引用
  demo/03-props-emit.html        父子传值（props + $emit）
  demo/04-vue-router.html        Vue Router 基础示例
  blog.html                      博客主页入口（组件化 + 路由）
  blog/components/               SiteHeader、PostCard、PostList、SearchBox、MessageBoard
  blog/views/                    HomeView、ArticleView、CategoryView、AboutView、MessageView、NotFoundView
  blog/router.js                 路由配置 + 根组件
  js/                            Vue 3、Vue Router 4 本地文件与模拟数据
  my-vue-blog/                   拓展：Vite + Vue 3 工程化项目
```

## 运行

- 示例页面：直接双击 `lab5/`、`lab6/` 下的 html 文件。
- Vite 工程：

```bash
cd lab6/my-vue-blog
npm install
npm run dev        # http://localhost:5173/
```
