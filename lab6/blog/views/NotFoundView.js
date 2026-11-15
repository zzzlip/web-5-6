/**
 * 路由视图：404
 */
const NotFoundView = {
  template: `
    <div class="card-block" style="text-align:center;padding:40px 20px">
      <h2 style="margin:0 0 8px">404</h2>
      <p>页面走丢了，<router-link to="/">返回首页</router-link></p>
    </div>
  `
};
