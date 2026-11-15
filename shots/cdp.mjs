// 极简 CDP 客户端：启动 Chrome headless，打开页面，执行动作，截图
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9333;

export async function launch() {
  const profile = '/tmp/dsh/chromeprofile2';
  fs.rmSync(profile, { recursive: true, force: true });
  const proc = spawn(CHROME, [
    '--headless=new', '--no-sandbox', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
    '--hide-scrollbars', '--force-device-scale-factor=1',
    `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`,
    '--window-size=1200,900', 'about:blank'
  ], { stdio: 'ignore' });
  let list;
  for (let i = 0; i < 100; i++) {
    try {
      list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
      if (list.some(t => t.type === 'page')) break;
    } catch (e) { /* retry */ }
    await new Promise(r => setTimeout(r, 200));
  }
  const page = list.find(t => t.type === 'page');
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
  let id = 0; const pending = new Map(); const logs = []; const waiters = [];
  ws.onmessage = ev => {
    const msg = JSON.parse(ev.data);
    if (msg.id && pending.has(msg.id)) {
      const { res, rej } = pending.get(msg.id); pending.delete(msg.id);
      msg.error ? rej(new Error(JSON.stringify(msg.error))) : res(msg.result);
    } else if (msg.method) {
      const s = JSON.stringify(msg.params);
      logs.push(`[${msg.method}] ${s.length > 500 ? s.slice(0, 500) + '…' : s}`);
      if (msg.method === 'Runtime.consoleAPICalled' || msg.method === 'Runtime.exceptionThrown') {
        lastConsole.push(msg.params);
      }
    }
  };
  const lastConsole = [];
  const send = (method, params = {}) => new Promise((res, rej) => {
    const i = ++id; pending.set(i, { res, rej });
    ws.send(JSON.stringify({ id: i, method, params }));
  });
  await send('Page.enable'); await send('Runtime.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: 1200, height: 900, deviceScaleFactor: 1, mobile: false });

  const api = {
    logs, lastConsole, send,
    async goto(url, w = 900) {
      await send('Page.navigate', { url });
      await new Promise(r => setTimeout(r, 1200));
    },
    async size(width, height) {
      await send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: false });
      await new Promise(r => setTimeout(r, 200));
    },
    async eval(expr) {
      const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
      if (r.exceptionDetails) throw new Error('eval error: ' + JSON.stringify(r.exceptionDetails).slice(0, 400));
      return r.result.value;
    },
    async type(selector, text) {
      await api.eval(`(() => { const el = document.querySelector(${JSON.stringify(selector)}); if(!el) throw new Error('no el '+${JSON.stringify(selector)}); el.focus(); el.value = ''; el.dispatchEvent(new Event('input', {bubbles:true})); return true; })()`);
      await api.eval(`(() => { const el = document.querySelector(${JSON.stringify(selector)}); el.value = ${JSON.stringify(text)}; el.dispatchEvent(new Event('input', {bubbles:true})); el.dispatchEvent(new Event('change', {bubbles:true})); return true; })()`);
      await new Promise(r => setTimeout(r, 250));
    },
    async key(selector, key) {
      await api.eval(`(() => { const el = document.querySelector(${JSON.stringify(selector)}); el.focus(); el.dispatchEvent(new KeyboardEvent('keydown', {key: ${JSON.stringify(key)}, bubbles:true})); el.dispatchEvent(new KeyboardEvent('keyup', {key: ${JSON.stringify(key)}, bubbles:true})); return true; })()`);
      await new Promise(r => setTimeout(r, 250));
    },
    async enter(selector) {
      await api.eval(`(() => { const el = document.querySelector(${JSON.stringify(selector)}); el.focus(); el.dispatchEvent(new KeyboardEvent('keydown', {key:'Enter', bubbles:true})); el.dispatchEvent(new KeyboardEvent('keyup', {key:'Enter', bubbles:true})); return true; })()`);
      await new Promise(r => setTimeout(r, 300));
    },
    async click(selector, index = 0) {
      await api.eval(`(() => { const els = document.querySelectorAll(${JSON.stringify(selector)}); if(!els[${index}]) throw new Error('no el ${selector} #${index}'); els[${index}].click(); return true; })()`);
      await new Promise(r => setTimeout(r, 350));
    },
    async hover(selector) {
      const r = await api.eval(`(() => { const el = document.querySelector(${JSON.stringify(selector)}); const b = el.getBoundingClientRect(); return [b.x + b.width/2, b.y + b.height/2]; })()`);
      await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: r[0], y: r[1] });
      await new Promise(r => setTimeout(r, 600));
    },
    async shot(file, fullPage = true, minH = 0) {
      const opts = { format: 'png' };
      if (fullPage) {
        const m = await send('Page.getLayoutMetrics');
        const h = Math.max(Math.ceil(m.cssContentSize.height), minH);
        opts.clip = { x: 0, y: 0, width: 1200, height: h, scale: 1 };
        opts.captureBeyondViewport = true;
      }
      const r = await send('Page.captureScreenshot', opts);
      fs.mkdirSync(path.dirname(file), { recursive: true });
      fs.writeFileSync(file, Buffer.from(r.data, 'base64'));
      console.log('saved', file);
    },
    async close() { try { ws.close(); } catch (e) {} proc.kill('SIGKILL'); }
  };
  return api;
}
