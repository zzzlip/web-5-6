# 实验5-6：Vue.js 基本语法、常用指令与组件、路由

## 目录说明

```
lab5/                     实验5：Vue.js 基本语法和常用指令
  index.html              常用指令综合练习（选项式 API、v-html/v-bind/v-if/v-for/v-on/v-model/v-text/v-show、computed/watch）
  blog.html               用 Vue 重构实验4的博客主页（博文列表 / 标题搜索 / 留言板）
  todo.html               选做：待办事项 TodoList（完成状态、编辑、分类统计）
  css/blog.css            博客样式
  js/vue-data.js          模拟数据
  js/vue.global.js        本地版 Vue（离线时使用）

lab6/                     实验6：组件和路由基础
  demo/01-options-api.html    选项式 API 基本结构
  demo/02-local-component.html 局部组件的定义、注册、引用
  demo/03-props-emit.html     父子传值（props + $emit）
  demo/04-vue-router.html     Vue Router 基础示例
  blog.html                   博客主页入口（组件化 + 路由）
  blog/components/            SiteHeader、PostCard、PostList、SearchBox、MessageBoard
  blog/views/                 HomeView、ArticleView、CategoryView、AboutView、MessageView、NotFoundView
  blog/router.js              路由配置 + 根组件
  my-vue-blog/                拓展：Vite + Vue 3 工程化项目

shots/                    运行截图（报告中引用的图片）及截图脚本
实验报告生成.py            生成实验报告 Word 文档的脚本
《WEB全栈开发技术》实验报告_Vue_实验5-6.docx   实验报告
```

## 运行方式

- 直接双击 lab5、lab6 下任意 `.html` 文件即可在浏览器中运行（脚本默认引用 `shots/vendor/` 下的 Vue 3.5.44 与 Vue Router 4.6.3）。
- 也可以把 `<script src=".../vue.global.js">` 换成 CDN 地址：`https://cdn.jsdelivr.net/npm/vue@3.5.44/dist/vue.global.js`。
- Vite 工程：

```bash
cd lab6/my-vue-blog
npm install
npm run dev        # 浏览器访问 http://localhost:5173/
```

## 环境

- Vue 3.5.44、Vue Router 4.6.3、Node.js 24、Chrome
