/**
 * 使用 Chrome DevTools 协议自动打开各实验页面、模拟操作并截图
 * 运行：node shots/capture.mjs
 */
import { launch } from './cdp.mjs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUT = path.join(ROOT, 'shots');
const url = p => 'file://' + path.join(ROOT, p).split('/').map(encodeURIComponent).join('/').replace(/^%2F/, '/').replace(/^file:%2F/, 'file:///');
const wait = ms => new Promise(r => setTimeout(r, ms));

const b = await launch();
const report = [];
async function shot(name, fullPage = true) {
  if (!fullPage) await b.eval('window.scrollTo(0, 0)');
  await b.shot(path.join(OUT, name), fullPage);
  report.push(name);
}

try {
  /* ---------------- 实验5 ---------------- */
  // 1. 基础指令
  await b.size(1200, 1000);
  await b.goto(url('lab5/index.html'));
  await wait(600);
  await b.type('#app input[type="text"]', '张小明');
  await b.eval("document.querySelector('#app').__vue_app && 0");
  await shot('lab5-01-基础指令.png');

  // 2. 博客主页：初始
  await b.size(1200, 1000);
  await b.goto(url('lab5/blog.html'));
  await wait(500);
  await shot('lab5-02-博客主页.png');

  // 3. 搜索
  await b.type('.search-bar input[type="text"]', 'vue');
  await wait(300);
  await shot('lab5-03-搜索vue.png');

  // 4. 搜索无结果
  await b.type('.search-bar input[type="text"]', 'Python');
  await wait(300);
  await shot('lab5-04-搜索无结果.png');

  // 5. 发表留言
  await b.eval("document.querySelector('.search-bar input').scrollIntoView()");
  await b.type('.message-form .nickname', '小明');
  await b.type('.message-form .content', 'Vue 的指令用起来真方便！');
  await b.click('.message-form button[type="submit"]');
  await wait(300);
  await b.eval("document.querySelector('.message-board').scrollIntoView({block:'center'})");
  await wait(300);
  await shot('lab5-05-发表留言.png', true);

  // 6. 删除留言
  await b.click('.message-list .del', 0);
  await wait(300);
  await shot('lab5-06-删除留言.png', true);

  // 7. TodoList
  await b.goto(url('lab5/todo.html'));
  await b.type('.todo-form input', '复习 v-for 与 v-model');
  await b.enter('.todo-form input');
  await wait(300);
  await b.click('.todos li:nth-child(2) input[type="checkbox"]');
  await wait(200);
  await b.click('.todos li:nth-child(3) .op', 0); // 编辑
  await wait(300);
  await b.eval("document.activeElement && document.activeElement.blur()");
  await wait(200);
  await shot('lab5-07-TodoList.png', true);

  /* ---------------- 实验6 ---------------- */
  // 选项式 API
  await b.goto(url('lab6/demo/01-options-api.html'));
  await wait(1200);
  await b.click('#app button', 1);   // 数量 +1
  await b.click('#app button', 1);   // 数量 +1
  await wait(300);
  await shot('lab6-01-选项式API.png', false);

  // 局部组件
  await b.goto(url('lab6/demo/02-local-component.html'));
  await b.click('#app1 button');
  await b.click('#app1 button');
  await b.click('#app2 button');
  await shot('lab6-02-局部组件.png', false);

  // 父子传值
  await b.goto(url('lab6/demo/03-props-emit.html'));
  await b.click('.user-card button');
  await wait(300);
  await shot('lab6-03-父子传值.png', false);

  // 路由基础
  await b.goto(url('lab6/demo/04-vue-router.html'));
  await b.eval("location.hash = '#/about'");
  await wait(500);
  await shot('lab6-04-路由about.png', false);
  await b.eval("location.hash = '#/article/2'");
  await wait(500);
  await shot('lab6-05-路由动态参数.png', false);

  // 博客组件化 + 路由
  await b.size(1200, 1000);
  await b.goto(url('lab6/blog.html'));
  await wait(500);
  await shot('lab6-06-组件化首页.png');
  await b.type('.search-bar input[type="text"]', 'CSS');
  await wait(300);
  await shot('lab6-07-组件化搜索.png');
  await b.eval("location.hash = '#/article/3'");
  await wait(600);
  await shot('lab6-08-文章详情.png');
  await b.eval("location.hash = '#/category'");
  await wait(600);
  await shot('lab6-09-分类.png');
  await b.eval("location.hash = '#/message'");
  await wait(600);
  await b.type('.message-form .nickname', 'Vue爱好者');
  await b.type('.message-form .content', '组件化之后结构清晰多了！');
  await b.click('.message-form button[type="submit"]');
  await wait(300);
  await shot('lab6-10-留言板.png');
  await b.eval("location.hash = '#/not-exist'");
  await wait(600);
  await shot('lab6-11-404.png');

  const errs = b.lastConsole.filter(m => JSON.stringify(m).includes('exception') || JSON.stringify(m).includes('error'));
  console.log('CONSOLE ERRORS:', JSON.stringify(errs).slice(0, 2000));
  console.log('DONE', report.length);
} finally {
  await b.close();
}
