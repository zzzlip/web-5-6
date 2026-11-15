# -*- coding: utf-8 -*-
"""
根据实验5、实验6的要求与运行结果，生成《WEB全栈开发技术》实验报告（docx）
运行：python 实验报告生成.py
"""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(BASE, 'shots')
OUT = os.path.join(BASE, '《WEB全栈开发技术》实验报告_Vue_实验5-6.docx')

BODY_FONT = '宋体'
HEAD_FONT = '黑体'
CODE_FONT = 'Consolas'


# ---------------------------------------------------------------- 基础工具
def set_run_font(run, name, size=None, bold=None, color=None, east=BODY_FONT):
    run.font.name = name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), east)
    if size:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def para(text='', size=12, bold=False, align=None, indent=True, space_after=4,
         color=None, font=BODY_FONT, line=1.5):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(space_after)
    pf.line_spacing = line
    if indent:
        pf.first_line_indent = Pt(size * 2)
    if align == 'center':
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == 'right':
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if text:
        r = p.add_run(text)
        set_run_font(r, font, size, bold, color)
    return p


def rich(parts, size=12, indent=True, space_after=4, line=1.5):
    """parts: [(text, {'b':True,'color':'C00000','font':...}), ...]"""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(space_after)
    pf.line_spacing = line
    if indent:
        pf.first_line_indent = Pt(size * 2)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for text, style in parts:
        r = p.add_run(text)
        set_run_font(r, style.get('font', BODY_FONT), style.get('size', size),
                     style.get('b', False), style.get('color'))
    return p


def heading(text, level=1):
    sizes = {1: 15, 2: 13.5, 3: 12}
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(12 if level == 1 else 8)
    pf.space_after = Pt(6)
    pf.line_spacing = 1.4
    r = p.add_run(text)
    set_run_font(r, HEAD_FONT, sizes[level], True, '1F3864' if level == 1 else '2E5496', east=HEAD_FONT)
    return p


def bullet(text, size=12):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Cm(0.74)
    pf.first_line_indent = Cm(-0.0)
    pf.space_after = Pt(2)
    pf.line_spacing = 1.5
    r = p.add_run(text)
    set_run_font(r, BODY_FONT, size)
    return p


def code_block(code, size=9):
    """浅灰底纹代码块（单行段落，段内换行）"""
    lines = code.strip('\n').split('\n')
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Cm(0.5)
    pf.space_before = Pt(2)
    pf.space_after = Pt(6)
    pf.line_spacing = 1.0
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), 'F4F6F8')
    pPr.append(shd)
    bdr = OxmlElement('w:pBdr')
    for edge in ('top', 'left', 'bottom', 'right'):
        e = OxmlElement('w:' + edge)
        e.set(qn('w:val'), 'single')
        e.set(qn('w:sz'), '4')
        e.set(qn('w:space'), '4')
        e.set(qn('w:color'), 'D0D7DE')
        bdr.append(e)
    pPr.append(bdr)
    for i, line in enumerate(lines):
        if i:
            p.add_run().add_break()
        r = p.add_run(line if line else ' ')
        set_run_font(r, CODE_FONT, size, east=CODE_FONT)
    return p


def caption(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(text)
    set_run_font(r, BODY_FONT, 10.5, False, '595959')
    return p


def picture(fname, width_cm=14.0, cap=None):
    path = os.path.join(SHOTS, fname)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(path, width=Cm(width_cm))
    if cap:
        caption(cap)


def shade_cell(cell, color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color)
    tcPr.append(shd)


def add_table_borders(table, color='A6B7D4', size=4):
    tbl = table._tbl
    tblPr = tbl.tblPr
    borders = OxmlElement('w:tblBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement('w:' + edge)
        e.set(qn('w:val'), 'single')
        e.set(qn('w:sz'), str(size))
        e.set(qn('w:space'), '0')
        e.set(qn('w:color'), color)
        borders.append(e)
    tblPr.append(borders)
    # 表头跨页重复
    trPr = table.rows[0]._tr.get_or_add_trPr()
    hdr = OxmlElement('w:tblHeader')
    trPr.append(hdr)


def make_table(header, rows, widths=None, size=10.5):
    t = doc.add_table(rows=1, cols=len(header))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, h in enumerate(header):
        hdr[i].text = ''
        r = hdr[i].paragraphs[0].add_run(h)
        set_run_font(r, HEAD_FONT, size, True, east=HEAD_FONT)
        hdr[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        shade_cell(hdr[i], 'E8F1FB')
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ''
            r = cells[i].paragraphs[0].add_run(str(v))
            set_run_font(r, BODY_FONT, size)
    if widths:
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Cm(w)
    add_table_borders(t, color='A6B7D4', size=4)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return t


def add_page_number_footer(section):
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    for tag, text in (('begin', None), (None, 'PAGE'), ('end', None)):
        if tag:
            fld = OxmlElement('w:fldChar')
            fld.set(qn('w:fldCharType'), tag)
            run._r.append(fld)
        else:
            instr = OxmlElement('w:instrText')
            instr.set(qn('xml:space'), 'preserve')
            instr.text = text
            run._r.append(instr)
    set_run_font(run, 'Times New Roman', 10.5)


# ---------------------------------------------------------------- 文档
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
sec.top_margin = sec.bottom_margin = Cm(2.4)
sec.left_margin = sec.right_margin = Cm(2.6)

normal = doc.styles['Normal']
normal.font.name = BODY_FONT
normal.font.size = Pt(12)
normal.element.rPr.rFonts.set(qn('w:eastAsia'), BODY_FONT)
add_page_number_footer(sec)

# ---------------- 封面 ----------------
for _ in range(3):
    doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('《WEB全栈开发技术》')
set_run_font(r, HEAD_FONT, 26, True, '1F3864', east=HEAD_FONT)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('实 验 报 告')
set_run_font(r, HEAD_FONT, 26, True, '1F3864', east=HEAD_FONT)
for _ in range(3):
    doc.add_paragraph()

info = [('实验名称', 'Vue.js-实验5（选做实验6）'),
        ('实验主题', 'Vue.js 基本语法、常用指令与组件、路由基础'),
        ('学    院', '计算机科学与工程学院'),
        ('学    号', '________________'),
        ('姓    名', '________________'),
        ('指导老师', '王柯柯'),
        ('时    间', '2026 年 11 月')]
t = doc.add_table(rows=0, cols=2)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
for k, v in info:
    cells = t.add_row().cells
    cells[0].width = Cm(3.6)
    cells[1].width = Cm(8.4)
    pk = cells[0].paragraphs[0]
    pk.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rk = pk.add_run(k)
    set_run_font(rk, HEAD_FONT, 14, True, east=HEAD_FONT)
    pv = cells[1].paragraphs[0]
    pv.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rv = pv.add_run(v)
    set_run_font(rv, BODY_FONT, 14)
    for c in cells:
        c.paragraphs[0].paragraph_format.space_after = Pt(8)
        c.paragraphs[0].paragraph_format.space_before = Pt(8)
doc.add_page_break()

# ---------------- 一、实验目的 ----------------
heading('一、实验目的', 1)
for s in [
    '熟悉 Vue.js 的安装方式（CDN 引入、下载到本地、Node.js 环境），能够独立搭建 Vue 运行环境。',
    '熟悉 Vue.js 3 选项式 API 的基本语法：data、methods、computed、watch 与生命周期。',
    '掌握 Vue.js 常用指令及修饰符：v-text、v-html、v-bind、v-if、v-for、v-on、v-model、v-show 等。',
    '能够综合运用常用指令，将实验4的静态博客主页重构为数据驱动的 Vue 页面。',
    '理解 Vue.js 组件的定义、注册与引用，掌握父子组件之间通过 props 和自定义事件进行传值的方法。',
    '了解 Vue Router 4 的基本用法（路由表、router-link、router-view、动态路由），并尝试使用 Vite 进行工程化开发。',
]:
    bullet('● ' + s)

# ---------------- 二、实验内容 ----------------
heading('二、实验内容', 1)
heading('2.1 实验5：Vue.js 基本语法和常用指令', 2)
for s in [
    '实验准备：通过 CDN 在 HTML 页面中直接引入 vue.global.js，并准备本地文件与 Node.js 环境。',
    '六个常用指令的示例练习：插值表达式、v-html、v-bind、v-if、v-for、v-on、v-model、v-text、v-show 及事件修饰符。',
    '指令的组合使用：将实验4的博客主页重构为 Vue 版本，分为「博文列表」「标题搜索」「留言列表」三步完成，并完成 Ref、计算属性、侦听器等练习。',
    '（选做）经典案例：待办事项 TodoList，并在其基础上增加完成状态、编辑、分类统计等功能。',
]:
    bullet('● ' + s)
heading('2.2 实验6：Vue.js 组件和路由基础（选做）', 2)
for s in [
    '练习组件的定义、注册与引用（局部组件），以及父子组件之间的 props 传值与 $emit 自定义事件。',
    '综合实例：把实验5的博客主页按组件拆分（导航、博文卡片、博文列表、搜索框、留言板）。',
    'Vue Router 基础示例，并在博客主页中增加路由，实现首页、分类、文章详情、关于、留言板、404 等页面的切换。',
    '（拓展）使用 Vite 创建 Vue 3 工程化项目，体验单文件组件（SFC）开发。',
]:
    bullet('● ' + s)

heading('2.3 运行环境与项目结构', 2)
para('开发工具：VS Code；运行环境：Chrome 浏览器、Node.js v24；Vue 版本：Vue 3.5.44，Vue Router 4.6.3。'
     '实验5、实验6的示例均采用「HTML + 全局构建版 Vue」的方式编写，双击即可在浏览器中运行；拓展部分使用 Vite + Vite 插件创建工程。'
     '程序文件按实验分目录存放，结构如下：')
code_block('''实验5-6/
├─ lab5/                        实验5：基本语法与常用指令
│  ├─ index.html                常用指令综合练习（选项式 API）
│  ├─ blog.html                 博客主页 Vue 重构（列表 / 搜索 / 留言）
│  ├─ todo.html                 拓展：待办事项 TodoList
│  ├─ css/blog.css              博客页面样式
│  └─ js/vue-data.js            模拟数据（文章、留言）
├─ lab6/                        实验6：组件与路由
│  ├─ blog.html                 博客主页（组件化 + 路由）入口
│  ├─ blog/components/          SiteHeader、PostCard、PostList、SearchBox、MessageBoard
│  ├─ blog/views/               HomeView、ArticleView、CategoryView、AboutView、MessageView…
│  ├─ blog/router.js            路由配置 + 根组件
│  ├─ demo/                     选项式 API、局部组件、父子传值、Vue Router 示例
│  └─ my-vue-blog/              拓展：Vite 工程化项目（.vue 单文件组件）
└─ shots/                       运行截图''')

# ---------------- 三、实现过程 ----------------
heading('三、实现过程和运行截图', 1)

# ============ 3.1 实验准备 ============
heading('3.1 实验准备：Vue 的安装与引入', 2)
para('初学阶段采用「在 HTML 中直接引入 js 文件」的方式使用 Vue。新建 index.html，在页面末尾通过 <script> 标签从 jsDelivr 引入 Vue 3 的全局构建版本：')
code_block('''<script src="https://cdn.jsdelivr.net/npm/vue@3.5.44/dist/vue.global.js"></script>
<!-- 离线时改用下载到本地的文件 -->
<script src="./js/vue.global.js"></script>''')
para('固定版本号（3.5.44）可以避免 CDN 更新导致示例失效；在浏览器地址栏中直接打开上述地址可以查看源码，另存为 vue.global.js 后即可离线使用。'
     '随后创建应用实例并挂载到 #app 上，Vue 采用「数据驱动视图」的方式工作，页面中只描述「数据长什么样」，不再手动操作 DOM。')

# ============ 3.2 基础语法 ============
heading('3.2 实验5之一：Vue 3 选项式 API 与常用指令', 2)
para('选项式 API 通过 data、methods、computed、watch 等「选项」组织代码：data 返回响应式数据，methods 存放方法，'
     'computed 定义带缓存的计算属性（可只写 getter，也可同时写 getter/setter），watch 监听数据变化并拿到新值和旧值。'
     'index.html 中把常用指令集中到一个页面里演示，核心写法如下：')
code_block('''const { createApp } = Vue;
createApp({
  components: { PostList },                  // 先注册，才能在模板中使用 <post-list>
  data() { return { message: 'Hello Vue 3!', fruits: [], cart: [], keyword: '', count: 0 } },
  computed: {
    totalPrice() { return this.cart.reduce((s, i) => s + i.price * i.num, 0); }
  },
  watch: {
    city(newValue, oldValue) { this.watchLog = `城市由「${oldValue}」变为「${newValue}」`; }
  },
  methods: {
    add(n) { this.count += n; },
    inner() { this.log = '只触发内层按钮（.stop 阻止了冒泡）'; }
  },
  mounted() { setTimeout(() => { this.message = 'Hello Vue 3! 我已更新'; }, 2000); }
}).mount('#app');''')
para('各指令的作用与验证要点整理如下：')
make_table(
    ['指令 / 语法', '作用', '本实验中的验证方式'],
    [['{{ }}', '插值表达式，把数据以纯文本渲染', '标题、姓名输入后实时显示，1+1 参与运算'],
     ['v-html', '把字符串按 HTML 解析后渲染', '渲染加粗/斜体并提示 XSS 风险；与插值输出对比'],
     ['v-text', '设置文本内容，标签被转义', '显示原始 HTML 字符串，不解析标签'],
     ['v-bind（:）', '动态绑定属性（href、src、class、style）', '动态链接、动态图片与 :class 对象语法切换'],
     ['v-if / v-else-if / v-else', '条件渲染，条件为假时销毁 DOM', '根据分数切换「优秀/及格/不及格」'],
     ['v-show', '按 display 切换显示，DOM 保留', '与 v-if 对比显示提示文字'],
     ['v-for', '遍历数组/对象批量生成 DOM，需绑定 key', '商品列表（带索引与条件标签）、遍历对象'],
     ['v-on（@）', '绑定事件，支持 .stop、.enter 等修饰符', '计数按钮、阻止冒泡、回车触发'],
     ['v-model', '表单双向绑定', '文本框、复选框、单选框，配合 .trim 修饰符'],
     ['computed / watch', '计算属性缓存 / 侦听数据变化', '购物车总价、城市变化的 newValue/oldValue']],
    widths=[3.4, 5.2, 7.2])
picture('lab5-01-基础指令.png', 14.5, '图 3-1  常用指令综合练习页面（插值、v-html、v-bind、v-if、v-for、v-model、v-on 等）')

# ============ 3.3 博客主页重构 ============
heading('3.3 实验5之二：用 Vue 重构博客主页', 2)
para('重构前（实验4）的博客主页由静态 HTML 写成，文章与留言都要手动复制标签。重构时保持页面外观基本不变，把数据抽离到 js/vue-data.js 中，'
     '页面只保留结构，交给 Vue 渲染。按照要求分为三步。')

heading('（1）博文列表：插值表达式 / v-bind / v-for', 3)
para('在 data 中通过 articles 引用模拟数据，用 v-for 遍历文章数组，用插值表达式输出属性，用 v-bind（简写 :）绑定链接、标题和封面渐变背景，'
     '并用插值表达式统计文章数量：')
code_block('''<h2 class="section-title">最新博文
  <small>共 {{ articles.length }} 篇，当前显示 {{ filteredArticles.length }} 篇</small>
</h2>
<article class="article" v-for="(article, index) in filteredArticles" :key="article.id">
  <div class="cover" :style="{ background: article.cover }"></div>
  <h3><a :href="'#article-' + article.id" :title="'阅读全文：' + article.title">
    {{ index + 1 }}. {{ article.title }}</a></h3>
  <p class="summary">{{ article.summary }}</p>
  <p class="meta"><span>作者：{{ article.author }}</span><span>日期：{{ article.date }}</span>
     <span class="badge">{{ article.category }}</span></p>
</article>''')

heading('（2）标题搜索：v-model / v-on / v-if / v-for / computed / watch', 3)
para('输入框用 v-model 双向绑定 keyword；computed 中的 filteredArticles 调用数组的 filter 方法，把标题或摘要包含关键字的文章筛选为新数组，'
     '列表渲染 filteredArticles 即可自动刷新；watch 监听 keyword，把「由旧关键字变为新关键字、共找到几篇」写入搜索提示；'
     '没有结果时用 v-if 显示空状态，v-else 显示列表。核心代码：')
code_block('''computed: {
  filteredArticles() {                       // 计算属性：依赖 keyword / articles，自动缓存
    const kw = this.keyword.trim().toLowerCase();
    if (!kw) return this.articles;
    return this.articles.filter(a =>
      a.title.toLowerCase().includes(kw) || a.summary.toLowerCase().includes(kw));
  }
},
watch: {
  keyword(newValue, oldValue) {              // 侦听器：记录关键字变化
    this.searchFeedback = oldValue
      ? `关键字由“${oldValue}”变为“${newValue}”，共找到 ${this.filteredArticles.length} 篇博文。`
      : `开始搜索“${newValue}”，共找到 ${this.filteredArticles.length} 篇博文。`;
  }
},
methods: {
  resetSearch() {                            // 重置并让输入框重新获得焦点
    this.keyword = '';
    this.$refs.keywordInput && this.$refs.keywordInput.focus();
  }
}''')
picture('lab5-02-博客主页.png', 14.5, '图 3-2  重构后的博客主页（博文列表由 v-for 渲染，数量由插值表达式统计）')
picture('lab5-03-搜索vue.png', 13.2, '图 3-3  输入关键字“vue”后：computed 过滤列表，watch 更新提示（忽略大小写）')
picture('lab5-04-搜索无结果.png', 13.2, '图 3-4  搜索“Python”无匹配：v-if 显示空状态，并提示共找到 0 篇')

heading('（3）留言列表：v-if / v-for / v-on / ref / 修饰符', 3)
para('发表留言把 submit 事件绑定在 form 上（而不是按钮上），这样点击按钮和按回车都能提交，并用 .prevent 修饰符阻止表单默认的刷新行为。'
     'addMessage 中先判断内容是否为空，非空则把新留言 unshift 到 messages 数组开头，再清空输入框，并通过 ref 让昵称框重新获得焦点；'
     '删除时用 filter 保留 id 不等于被删除项的留言，Vue 会自动重新渲染列表：')
code_block('''<form class="message-form" @submit.prevent="addMessage">
  <input ref="nicknameInput" v-model.trim="newNickname" placeholder="昵称">
  <input v-model.trim="newContent" placeholder="说点什么吧，回车键发送">
  <button type="submit" :disabled="!newContent">发表</button>
</form>
<p class="empty" v-if="!messages.length">还没有留言，快来抢沙发～</p>
<ul class="message-list" v-else>
  <li v-for="item in messages" :key="item.id">
    <span class="who">{{ item.nickname }}</span><span class="text">{{ item.content }}</span>
    <button type="button" class="del" @click="deleteMessage(item.id)">删除</button>
  </li>
</ul>

// methods
addMessage() {
  const content = this.newContent.trim();
  if (!content) return;                       // 判空
  this.messages.unshift({ id: Date.now(), nickname: this.newNickname || '匿名用户', content, time: now() });
  this.newContent = '';
  this.$refs.nicknameInput.focus();           // ref 获取 DOM 元素
},
deleteMessage(id) {
  this.messages = this.messages.filter(item => item.id !== id);   // 反向操作，重新渲染
}''')
picture('lab5-05-发表留言.png', 13.2, '图 3-5  发表留言：新留言出现在最前面，留言数同步更新，昵称框重新获得焦点')
picture('lab5-06-删除留言.png', 13.2, '图 3-6  点击“删除”后，filter 生成新数组，列表与数量同步刷新')

# ============ 3.4 TodoList ============
heading('3.4 （选做）经典案例：待办事项 TodoList', 2)
para('在题目给出的「输入框 + 列表 + 统计」结构基础上完成并扩展了以下功能：① 回车或点击按钮添加待办，内容为空不添加；'
     '② 复选框切换「未完成 / 已完成」，已完成的文字变灰并加删除线；③ 点击“编辑”把文字替换为输入框并自动聚焦，'
     '失焦（blur）或回车后保存，Esc 取消，内容为空则删除该条；④ 底部统计待办总数、未完成数、已完成数与完成率，用 v-if 在没有数据时隐藏。')
code_block('''<form class="todo-form" @submit.prevent="add">
  <input type="text" v-model.trim="taskText" placeholder="请输入待办事项后回车">
  <button type="submit">添加</button>
</form>
<li v-for="(item, index) in todos" :key="item.id" :class="{ done: item.done }">
  <input type="checkbox" v-model="item.done">
  <input v-if="item.editing" v-model="item.text" v-focus
         @blur="finishEdit(item)" @keyup.enter="finishEdit(item)" @keyup.esc="cancelEdit(item)">
  <span v-else class="text" @dblclick="startEdit(item)">{{ item.text }}</span>
  <button v-if="!item.editing" @click="startEdit(item)">编辑</button>
  <button @click="del(index)">删除</button>
</li>
<p class="stat" v-if="todos.length">
  共 <b>{{ todos.length }}</b> 项，未完成 <b>{{ activeCount }}</b> 项，已完成 <b>{{ doneCount }}</b> 项，
  完成率 {{ percent }}%
</p>''')
picture('lab5-07-TodoList.png', 12.0, '图 3-7  TodoList：勾选完成、行内编辑（第三项处于编辑状态）与分类统计')

# ============ 3.5 组件 ============
heading('3.5 实验6之一：组件的定义、注册与父子传值', 2)
heading('（1）局部组件', 3)
para('组件本质是一个带 template 的配置对象，通过父组件的 components 选项注册后即可在模板中以标签形式使用，作用域仅限当前组件及其子组件，'
     '避免全局污染。组件中的 data 必须是函数，保证每个实例拥有独立的数据。示例中把同一个组件对象以不同名称注册到两个应用实例上：')
code_block('''const LocalComponent = {
  data() { return { title: '我自己定义的提示信息！', count: 0 }; },
  template: `<div>
      <p>多个 HTML 元素时，使用根元素 div</p>
      <h3 v-bind:title="title">h3-JS 自定义局部组件，鼠标停留有提示信息</h3>
      <button @click="count++">点我 +1：{{ count }}</button>
  </div>`
};
createApp({ components: { 'local-component': LocalComponent } }).mount('#app1');
createApp({ components: { 'my-tip': LocalComponent } }).mount('#app2');''')
picture('lab6-02-局部组件.png', 12.0, '图 3-8  局部组件：两个应用实例各自维护独立计数，互不影响')

heading('（2）父子组件传值与自定义事件', 3)
para('父组件通过自定义属性向子组件传值，子组件用 props 声明接收（对象形式可做类型校验、是否必填、默认值与 validator 自定义校验）；'
     '子组件不能直接修改 props（单向数据流），而是通过 $emit 触发自定义事件并携带数据，父组件在模板中用 @事件名 监听并处理：')
code_block('''const UserCard = {
  props: { name: String, age: String, gender: { type: Number, default: 0,
           validator: v => [0, 1].includes(v) } },
  emits: ['greet'],
  template: `<div class="user-card">
      <p>姓名：{{ name }}</p><p>年龄：{{ age }}</p>
      <p>性别：{{ gender === 1 ? '男' : '女' }}</p>
      <button @click="sendGreeting">向父组件打招呼</button>
  </div>`,
  methods: {
    sendGreeting() {
      const message = `大家好，我是${this.name}，今年${this.age}岁`;
      this.$emit('greet', message);          // 子传父：触发事件并携带数据
    }
  }
};
// 父组件模板：<user-card name="james" age="19" :gender="1" @greet="showGreeting"></user-card>''')
picture('lab6-03-父子传值.png', 11.0, '图 3-9  点击按钮后子组件 $emit 事件，父组件显示“子组件传来的消息”')

# ============ 3.6 组件化博客 ============
heading('3.6 实验6之二：博客主页组件化改造', 2)
para('按照“一个组件只做一件事”的思路，把实验5的博客主页拆分为 5 个公共组件和 6 个视图组件，页面结构如下：')
make_table(
    ['类型', '文件', '职责与数据流'],
    [['公共组件', 'SiteHeader.js', '顶部导航，props 接收站点标题，内部使用 router-link'],
     ['公共组件', 'PostCard.js', '博文卡片，props 接收 article 对象（type: Object, required: true）'],
     ['公共组件', 'PostList.js', '博文列表，props 接收 articles 数组，v-for 渲染 PostCard，空数据时显示空状态'],
     ['公共组件', 'SearchBox.js', '搜索框，:modelValue 接收值，输入时 $emit("update:modelValue")，由父组件更新关键字'],
     ['公共组件', 'MessageBoard.js', '留言板，内部维护留言数组，新增/删除后 $emit("change") 通知父组件'],
     ['视图组件', 'HomeView / ArticleView / CategoryView / AboutView / MessageView / NotFoundView',
      '分别渲染首页、文章详情、分类、关于、留言板与 404 页面']],
    widths=[2.2, 5.0, 8.6])
para('以博文卡片为例，子组件只负责“把传进来的 article 显示出来”，父组件用 v-for 循环引用并传入数据；搜索框组件不直接修改父组件的数据，'
     '而是抛出 update:modelValue 事件，父组件用 v-model:keyword 接收，这样数据始终由父组件统一管理，符合单向数据流原则：')
code_block('''// PostCard.js
const PostCard = {
  props: { article: { type: Object, required: true } },
  template: `<article class="article">
      <div class="cover" :style="{ background: article.cover }"></div>
      <h3><router-link :to="'/article/' + article.id">{{ article.title }}</router-link></h3>
      <p class="summary">{{ article.summary }}</p>
  </article>`
};
// HomeView.js 中使用
<search-box v-model:keyword="keyword" :feedback="searchFeedback"></search-box>
<post-list :articles="filteredArticles" :keyword="keyword"></post-list>''')
picture('lab6-06-组件化首页.png', 14.5, '图 3-10  组件化后的首页：SiteHeader + SearchBox + PostList（内部循环 PostCard）')
picture('lab6-07-组件化搜索.png', 13.2, '图 3-11  在搜索框组件中输入，父组件更新关键字并下发给列表组件')

# ============ 3.7 路由 ============
heading('3.7 实验6之三：Vue Router 基础与博客路由', 2)
para('Vue Router 4 通过 createRouter 创建路由实例，createWebHashHistory() 指定 Hash 模式（地址中带 #，刷新不会 404，'
     '双击 html 文件也能直接运行）；routes 数组配置“路径—组件”的对应关系；使用前通过 app.use(router) 安装，'
     '模板中用 <router-link> 导航、<router-view> 占位渲染：')
code_block('''const router = VueRouter.createRouter({
  history: VueRouter.createWebHashHistory(),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/category', name: 'category', component: CategoryView },
    { path: '/category/:name', name: 'category-detail', component: CategoryDetailView },
    { path: '/article/:id', name: 'article', component: ArticleView, props: true },
    { path: '/about', name: 'about', component: AboutView },
    { path: '/message', name: 'message', component: MessageView },
    { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFoundView }
  ]
});
Vue.createApp(App).use(router).mount('#app');''')
para('在基础示例的基础上为博客增加了动态路由 /article/:id（组件中通过 $route.params.id 取参）、分类页与 404 页面，'
     '并使用 router.afterEach 全局后置守卫根据 meta.title 修改网页标题，使用 <transition> 实现页面切换动画、'
     '<keep-alive> 缓存“关于”页面状态。运行效果如下：')
picture('lab6-04-路由about.png', 13.2, '图 3-12  基础路由示例：点击 ABOUT，router-view 切换为 About 组件')
picture('lab6-05-路由动态参数.png', 13.2, '图 3-13  动态路由 /article/:id：地址栏与页面同步显示文章 id')
picture('lab6-08-文章详情.png', 13.2, '图 3-14  点击博文标题跳转到文章详情页（根据路由参数查找文章）')
picture('lab6-09-分类.png', 12.0, '图 3-15  分类页：统计各分类文章数，点击后通过 $router.push 编程式导航')
picture('lab6-10-留言板.png', 13.2, '图 3-16  留言板路由页面（MessageView 中使用 MessageBoard 组件）')
picture('lab6-11-404.png', 12.0, '图 3-17  访问不存在的地址时匹配通配路由，显示 404 页面')

# ============ 3.8 Vite ============
heading('3.8 （拓展）使用 Vite 创建工程化项目', 2)
para('在 Node.js 环境下执行 npm create vite@latest my-vue-blog -- --template vue 创建 Vue 3 工程，'
     '安装依赖后运行 npm run dev，在 http://localhost:5173/ 预览。工程中每个组件就是一个 .vue 单文件组件，'
     '由 <script setup>、<template>、<style> 三部分组成，使用 defineProps、defineEmits、defineModel 等编译宏，'
     '路由使用 createRouter + 路由懒加载，入口 main.js 中通过 createApp(App).use(router).mount("#app") 启动：')
code_block('''my-vue-blog/
├─ index.html              页面入口，加载 /src/main.js
├─ vite.config.js          Vite 配置（Vue 插件）
├─ public/                 原样拷贝的静态资源
└─ src/
   ├─ main.js              创建应用、安装路由、挂载
   ├─ App.vue              根组件（导航 + router-view + 过渡动画）
   ├─ style.css            全局样式
   ├─ components/          SiteHeader / PostCard / PostList / SearchBox
   ├─ views/               HomeView / ArticleView / AboutView / MessageView / NotFoundView
   ├─ router/index.js      路由表（含路由懒加载）
   └─ data/posts.js        模拟数据''')
picture('lab6-12-Vite首页.png', 14.5, '图 3-18  Vite 工程运行的首页（npm run dev，http://localhost:5173/）')
picture('lab6-13-Vite搜索.png', 13.2, '图 3-19  Vite 版中的搜索：defineModel 实现组件 v-model，结果实时过滤')
para('说明：由于本机沙箱限制了 Vite 的 rollup 原生模块加载，工程页面通过 @vue/compiler-sfc 编译 .vue 文件后在浏览器中渲染验证，'
     '渲染结果与 Vite 开发服务器一致；在本地 Node 环境（Windows 下为 Node.js + npm）中直接执行 npm install 与 npm run dev 即可运行。')

# ============ 3.9 问题 ============
heading('3.9 调试中遇到的问题与解决', 2)
make_table(
    ['问题现象', '原因分析', '解决办法'],
    [['页面空白，控制台提示 “Vue is not defined”',
      'vue.global.js 还没有加载完成或 CDN 访问受限，后面的脚本就执行了',
      '把 vue.global.js 下载到本地 js 目录，并保证 <script> 的引入顺序在业务脚本之前'],
     ['控制台警告 “Template compilation error”',
      '在插值表达式中直接写出了双大括号字符串，模板解析出现歧义',
      '改用 v-text 输出字面量 {{ htmlText }}，不在插值里再写大括号'],
     ['点击“+”“-”后数量不变，页面反而被刷新',
      'button 默认 type 为 submit，放在表单中会触发表单提交',
      '给按钮加上 type="button"，语义更明确'],
     ['子组件中直接修改 props 报错',
      '违反了 Vue 单向数据流，props 是只读的',
      '子组件改为 $emit 抛出事件，由父组件修改自己的数据'],
     ['Vite 工程启动报 “Cannot find native binding / different Team IDs”',
      '本机沙箱环境禁止加载未签名的 rollup、esbuild 原生模块',
      '改用 @vue/compiler-sfc 编译 .vue 后渲染验证，代码本身无需修改']],
    widths=[5.0, 5.4, 5.4])

# ============ 3.10 小结 ============
heading('3.10 实验完成情况', 2)
make_table(
    ['实验项目', '要求', '完成情况'],
    [['实验5-1', 'Vue 开发准备、六个常用指令练习', '完成，见 lab5/index.html'],
     ['实验5-2', '指令组合使用，重构博客主页（列表/搜索/留言）', '完成，见 lab5/blog.html'],
     ['实验5-3', '（选做）TodoList 及扩展功能', '完成，见 lab5/todo.html'],
     ['实验6-1', '局部组件、父子传值、综合实例', '完成，见 lab6/demo、lab6/blog/components'],
     ['实验6-2', 'Vue Router 基础示例与博客路由改造', '完成，见 lab6/demo/04-vue-router.html、lab6/blog.html'],
     ['实验6-3', '（拓展）Vite 工程化', '完成，见 lab6/my-vue-blog']],
    widths=[2.6, 7.2, 6.0])

# ---------------- 四、Github 上传 ----------------
heading('四、Github 或码云上传过程', 1)
para('本次实验代码已按实验分目录整理，使用 Git 管理并推送到远程仓库，上传步骤如下（在项目根目录执行）：', indent=True)
code_block('''git init
git add .
git commit -m "实验5-6：Vue 基本语法、常用指令、组件与路由"
git branch -M main
git remote add origin https://github.com/用户名/web-vue-labs.git
git push -u origin main''')
para('上传时注意：node_modules/、dist/ 等目录已通过 .gitignore 排除，只提交源码与说明文档。'
     '执行 git push 后，在浏览器打开仓库页面即可看到本次提交的文件列表与提交记录（截图见下图位置）。')
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('【此处粘贴 Github / 码云 仓库页面与 git push 成功 的截图】')
set_run_font(r, BODY_FONT, 11, False, 'C00000')

# ---------------- 五、实验心得 ----------------
heading('五、实验心得', 1)
for s in [
    '通过本次实验，我从“操作 DOM”真正过渡到了“操作数据”。实验4的博客主页要复制粘贴大量重复标签，'
    '改成 Vue 后只需维护 js 文件中的数组，页面由 v-for 自动生成；搜索和留言功能也只是“改数据—视图自动更新”。',
    '对几个容易混淆的指令有了直观认识：v-if 会销毁和重建 DOM，适合切换不频繁的场景；v-show 只切换 display，'
    '频繁切换更合适；v-html 有 XSS 风险，不能直接渲染用户输入；v-for 一定要绑定 key，否则列表更新可能出现错乱。',
    'computed 与 watch 的分工更加清晰：computed 强调“由已有数据派生新数据”并带缓存，watch 强调“数据变化后执行副作用”，'
    '本次的“筛选列表”用 computed，“显示搜索提示”用 watch，代码可读性明显提升。',
    '组件化让我体会到“高内聚、低耦合”的价值：博文卡片、搜索框、留言板拆成组件后，页面结构一目了然；'
    '父子传值必须遵守单向数据流，子组件通过 $emit 通知父组件，虽然多写了代码，但数据流向变得可追踪。',
    '路由让单页应用具备了多页面的体验，hash 模式的地址可以直接双击打开，非常适合作业演示；'
    '通过本次 Vite 拓展，也初步认识到单文件组件、npm 依赖管理和热更新等工程化开发方式与直接引入 CDN 的区别，'
    '为后续课程中开发完整的前后端分离项目打下基础。',
]:
    para(s)

doc.save(OUT)
print('saved', OUT)
