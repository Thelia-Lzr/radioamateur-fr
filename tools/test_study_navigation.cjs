/* NODE_PATH=/path/to/node_modules node tools/test_study_navigation.cjs */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {JSDOM} = require('jsdom');
const root = path.join(__dirname, '..');
const manual = fs.readFileSync(path.join(root, 'manuel-zh.html'), 'utf8');
const notebook = fs.readFileSync(path.join(root, 'mistake-book.html'), 'utf8');
const script = fs.readFileSync(path.join(root, 'source/study_navigation.js'), 'utf8');
const sidebar = manual.match(/<button[^>]*class="sidebar-toggle"[\s\S]*?<button[^>]*class="sidebar-backdrop"[\s\S]*?<\/button>/)[0];
const pause = () => new Promise(resolve => setTimeout(resolve, 35));
function fixture({mobile=false, hash=''}={}) {
  const dom = new JSDOM(sidebar + '<main><h2 id="avant-propos">首页</h2><h2 id="chap-R-4">法规 R-4</h2>' +
    '<h3 id="R45">考试组织</h3><details id="extra"><summary>其余题目</summary><h3 id="T126">调制方式</h3></details>' +
    '<section id="radio-glossary"><h2>附录 H</h2><h3 id="glossary-A">A</h3></section>' +
    '<a href="#T126" id="deep">展开并跳转</a><a href="#missing" id="invalid">无效链接</a></main>',
    {url:'https://offline.test/manuel-zh.html'+hash, runScripts:'outside-only', pretendToBeVisual:true});
  const win = dom.window;
  win.__y = 0;
  win.__shift = 0;
  win.scrollTo = (x,y) => { win.__y=y; win.__calls=(win.__calls||0)+1; };
  Object.defineProperty(win, 'scrollY', {get:()=>win.__y});
  win.matchMedia = () => ({matches:mobile, addEventListener(){}});
  win.__observers = [];
  win.ResizeObserver = class {
    constructor(callback){ this.callback=callback; win.__observers.push(this); }
    observe(){} disconnect(){this.disconnected=true;}
  };
  for (const [id, top] of [['avant-propos',0],['chap-R-4',3000],['R45',3500],['T126',6000],['radio-glossary',8000],['glossary-A',8200]]) {
    const node = win.document.getElementById(id);
    node.getClientRects = () => node.closest('details:not([open])') ? [] : [{}];
    node.getBoundingClientRect = () => ({top:top+win.__shift-win.__y});
  }
  let resolveMath;
  win.MathJax = {startup:{promise:new Promise(resolve=>{resolveMath=resolve;})}};
  win.__resolveMath=resolveMath;
  win.eval(script);
  return dom;
}
function click(dom, selector) { dom.window.document.querySelector(selector).click(); }
(async () => {
  // Parse the delivered files with HTML5 rules, including their complete heading structure.
  for (const [name, text] of [['manual',manual],['notebook',notebook]]) {
    const sanitized = text.replace(/<script\b[^>]*>[\s\S]*?<\/script>/g,'').replace(/data:image\/png;base64,[^"]+/g,'');
    const dom = new JSDOM(sanitized);
    const doc = dom.window.document;
    assert.equal(doc.querySelectorAll('#study-sidebar').length,1,name);
    assert.equal(doc.querySelectorAll('[data-mistake-link]').length,2,name);
    assert.ok(doc.querySelector('#study-sidebar [data-mistake-link]'),name);
    const shortcuts=doc.querySelector('.sidebar-shortcuts');
    assert.equal(shortcuts.children[2].getAttribute('data-mistake-link'),'mock-exam.html');
    assert.equal(doc.querySelector('main .toc'),null,name);
    if (name==='manual') {
      assert.equal(doc.querySelectorAll('.toc-chapter').length,18);
      for (const link of doc.querySelectorAll('.toc a[href^="#"]')) {
        const target=doc.getElementById(link.hash.slice(1));
        assert.ok(target && doc.querySelector('main').contains(target),link.hash);
        assert.equal(target.closest('details'),null,link.hash+' unexpectedly hidden by HTML parsing');
        const label=link.textContent.trim().split(/\s/)[0];
        if (/^#(?:chap-|[RT]\d)/.test(link.hash)) {
          assert.ok(target.textContent.trim().startsWith(label),link.hash+' points to a different heading');
        }
      }
      assert.equal(doc.querySelectorAll('img.qimg[width][height]').length,2688);
    }
    dom.window.close();
  }
  const desktop=fixture();
  const doc=desktop.window.document;
  assert.equal(doc.body.dataset.sidebarOpen,'true');
  click(desktop,'[data-sidebar-toggle]');
  assert.equal(doc.body.dataset.sidebarOpen,'false');
  assert.equal(doc.querySelector('[data-sidebar-toggle]').getAttribute('aria-expanded'),'false');
  assert.equal(doc.getElementById('study-sidebar').inert,true);
  click(desktop,'[data-sidebar-toggle]');
  assert.equal(doc.body.dataset.sidebarOpen,'true');
  click(desktop,'.toc a[href="#R45"]');
  await pause();
  assert.equal(desktop.window.location.hash,'#R45');
  assert.equal(desktop.window.__y,3476);
  assert.equal(doc.activeElement.id,'R45');
  assert.equal(doc.querySelector('.toc a[href="#R45"]').getAttribute('aria-current'),'location');
  assert.equal(doc.querySelector('.toc a[href="#R45"]').closest('details').open,true);
  // Images can change the document height after a click; keep the chosen heading at 24 px.
  desktop.window.__shift=430;
  desktop.window.__observers.at(-1).callback();
  await pause();
  assert.equal(desktop.window.__y,3906);
  // Formula typesetting can complete later, including after image correction.
  desktop.window.__shift=600;
  desktop.window.__resolveMath();
  await pause();
  assert.equal(desktop.window.__y,4076);
  desktop.window.dispatchEvent(new desktop.window.WheelEvent('wheel'));
  desktop.window.__shift=900;
  desktop.window.__observers.at(-1).callback();
  await pause();
  assert.equal(desktop.window.__y,4076,'must not pull the reader back after manual scrolling');
  click(desktop,'#deep');
  await pause();
  assert.equal(doc.getElementById('extra').open,true);
  assert.equal(desktop.window.__y,6876);
  // Back/forward hash changes and initial deep links use the same correction path.
  desktop.window.history.replaceState(null,'','#R45');
  desktop.window.dispatchEvent(new desktop.window.HashChangeEvent('hashchange'));
  await pause();
  assert.equal(desktop.window.__y,4376);
  click(desktop,'.toc a[href="#radio-glossary"]');
  await pause();
  assert.equal(desktop.window.__y,8876);
  assert.equal(doc.querySelector('.toc a[href="#radio-glossary"]').getAttribute('aria-current'),'location');
  desktop.window.__y=9150;
  desktop.window.dispatchEvent(new desktop.window.WheelEvent('wheel'));
  desktop.window.dispatchEvent(new desktop.window.Event('scroll'));
  await pause();
  assert.equal(doc.querySelector('.toc a[href="#radio-glossary"]').getAttribute('aria-current'),'location');
  const initial=fixture({hash:'#R45'});
  await pause();
  assert.equal(initial.window.__y,3476);
  const phone=fixture({mobile:true});
  assert.equal(phone.window.document.body.dataset.sidebarOpen,'false');
  click(phone,'[data-sidebar-toggle]');
  click(phone,'.toc a[href="#R45"]');
  await pause();
  assert.equal(phone.window.document.body.dataset.sidebarOpen,'false');
  assert.equal(phone.window.__y,3476);
  click(phone,'[data-sidebar-toggle]');
  phone.window.document.querySelector('.toc summary').dispatchEvent(new phone.window.KeyboardEvent('keydown',{key:'Escape',bubbles:true}));
  assert.equal(phone.window.document.body.dataset.sidebarOpen,'false');
  assert.equal(phone.window.document.activeElement,phone.window.document.querySelector('[data-sidebar-toggle]'));
  for (const dom of [desktop,initial,phone]) dom.window.close();
  console.log('通过：18 章目录的 HTML5 锚点、侧栏折叠、窄屏关闭、深链与历史跳转、隐藏内容展开、图片／公式排版校正及主动滚动取消。');
})().catch(error=>{console.error(error);process.exitCode=1;});
