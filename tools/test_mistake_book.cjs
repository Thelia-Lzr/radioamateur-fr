/* Run with jsdom installed: NODE_PATH=/path/to/node_modules node tools/test_mistake_book.cjs */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { JSDOM } = require('jsdom');
const root = path.join(__dirname, '..');
const manual = fs.readFileSync(path.join(root, 'manuel-zh.html'), 'utf8');
const fixtures = manual.matchAll(/<li class="exam-question"[^>]*>.*?<\/details>\s*<\/li>/gs);
const samples = [fixtures.next().value[0], fixtures.next().value[0]];
const ids = samples.map(s => s.match(/data-question="(\d+)"/)[1]);
const mistakesScript = fs.readFileSync(path.join(root, 'source/quiz_mistakes.js'), 'utf8');
const quizScript = manual.match(/<script id="manual-quiz-script">([\s\S]*?)<\/script>/)[1];
const storageKey = 'radioamateur-fr.mistakes.v1';
function page({book=false, hash='', saved=null, blocked=false}={}) {
  const content = book ? '<template id="mistake-bank"><ol>'+samples.join('')+'</ol></template>'+
    '<div class="exam"><ol id="mistake-questions"></ol></div><p id="mistake-empty"></p><p id="mistake-missing"></p><button id="mistake-retry"></button>' : '<h3 id="R11">测试章节</h3><details class="all-lesson-questions"><summary>其余题目</summary><div class="exam"><ol>'+samples.join('')+'</ol></div></details>';
  const dom = new JSDOM('<main><b data-mistake-count></b><p data-mistake-storage hidden></p>'+content+'</main>',
    {url:'https://offline.test/'+(book?'mistake-book.html':'manuel-zh.html')+hash, runScripts:'outside-only', pretendToBeVisual:true});
  if(book) dom.window.document.body.setAttribute('data-mistake-book','');
  if(saved!==null) dom.window.localStorage.setItem(storageKey,saved);
  if(blocked) Object.defineProperty(dom.window,'localStorage',{get(){throw Error('blocked');}});
  dom.window.scrollTo = function(x,y) { dom.window.__restoredY = y; };
  dom.window.eval(mistakesScript);
  dom.window.eval(quizScript);
  return dom;
}
function click(dom, selector) { dom.window.document.querySelector(selector).click(); }
function count(dom) { return Number(dom.window.document.querySelector('[data-mistake-count]').textContent); }
let dom = page();
assert.ok(dom.window.document.querySelector('.quiz-selection-nav [data-mistake-link]'));
assert.equal(dom.window.document.querySelector('.quiz-selection-nav').hidden,false);
assert.equal(count(dom),0);
click(dom,'[data-action="mistake"]');
assert.equal(count(dom),1);
assert.equal(dom.window.document.querySelector('[data-action="mistake"]').getAttribute('aria-pressed'),'true');
const saved = dom.window.localStorage.getItem(storageKey);
const notebookUrl = new URL(dom.window.document.querySelector('[data-mistake-link]').href);
// Persisted marks survive reopening; choosing a wrong answer alone does not add a manual mark.
let reopened=page({saved}); assert.equal(count(reopened),1);
const second = reopened.window.document.querySelectorAll('.exam-question')[1];
second.querySelector('.quiz-choice:not([data-ok])').click();
assert.equal(count(reopened),1);
// Snapshot handoff works with empty, isolated storage on the other page.
let book = page({book:true,hash:notebookUrl.hash});
assert.equal(book.window.document.querySelectorAll('.exam-question').length,1);
assert.equal(book.window.document.querySelector('.exam-question').dataset.question,ids[0]);
assert.equal(book.window.document.querySelectorAll('.picked-right,.picked-wrong').length,0);
assert.equal(book.window.document.querySelector('.quiz-answer').open,false);
assert.equal(book.window.document.querySelector('.exam-question').firstElementChild.className,'quiz-image');
click(book,'.quiz-choice[data-ok="1"]');
assert.equal(book.window.document.querySelectorAll('.picked-right').length,1);
click(book,'[data-action="reset"]');
assert.equal(book.window.document.querySelectorAll('.picked-right').length,0);
click(book,'[data-action="mistake"]');
assert.equal(count(book),0);
assert.equal(book.window.document.querySelectorAll('.exam-question').length,1); // retain this round
const backHash = new URL(book.window.document.querySelector('[data-mistake-link]').href).hash;
let returned=page({hash:backHash,saved}); assert.equal(count(returned),0);
let empty=page({book:true,hash:backHash}); assert.equal(empty.window.document.querySelectorAll('.exam-question').length,0);
assert.equal(empty.window.document.getElementById('mistake-empty').hidden,false);
let invalid=page({hash:'#marks=%5B%22bad%22%2C%22'+ids[0]+'%22%2C%22'+ids[0]+'%22%5D'});
assert.equal(count(invalid),1);
let malformed=page({hash:'#marks=%7Bbroken',saved}); assert.equal(count(malformed),1);
let blocked=page({blocked:true}); click(blocked,'[data-action="mistake"]'); assert.equal(count(blocked),1);
assert.equal(blocked.window.document.querySelector('[data-mistake-storage]').hidden,false);
assert.ok(new URL(blocked.window.document.querySelector('[data-mistake-link]').href).hash.includes(ids[0]));
// An update in another tab refreshes button state and the notebook link.
reopened.window.localStorage.setItem(storageKey,'[]');
reopened.window.dispatchEvent(new reopened.window.StorageEvent('storage',{key:storageKey}));
assert.equal(count(reopened),0);
for(const instance of [dom,reopened,book,returned,empty,invalid,malformed,blocked]) instance.window.close();
(async function () {
  let reading=page();
  const doc=reading.window.document;
  const heading=doc.getElementById('R11');
  const question=doc.querySelector('.exam-question');
  const image=question.querySelector('.quiz-image');
  doc.querySelector('.all-lesson-questions').open=true;
  for(const [node,top] of [[heading,-900],[question,-350],[image,-340]]) {
    node.getClientRects=()=>[{top}]; node.getBoundingClientRect=()=>({top});
  }
  click(reading,'[data-action="mistake"]');
  const link=doc.querySelector('.quiz-selection-nav [data-mistake-link]');
  link.addEventListener('click',e=>e.preventDefault());
  link.click();
  const outbound=new URL(link.href);
  const position=JSON.parse(new URLSearchParams(outbound.hash.slice(1)).get('return'));
  assert.equal(position.anchor,image.id); assert.equal(position.offset,-340);
  let reviewing=page({book:true,hash:outbound.hash});
  const returnLink=reviewing.window.document.querySelector('.quiz-selection-nav [data-mistake-link]');
  assert.equal(returnLink.textContent,'返回教材');
  const returnUrl=new URL(returnLink.href);
  assert.deepEqual(JSON.parse(new URLSearchParams(returnUrl.hash.slice(1)).get('return')),position);
  // The refreshed notebook remembers the origin even after the URL snapshot was consumed.
  const remembered=reviewing.window.sessionStorage.getItem(storageKey+'.return');
  assert.deepEqual(JSON.parse(remembered),position);
  let restored=page({hash:returnUrl.hash});
  const restoredImage=restored.window.document.getElementById(image.id);
  restoredImage.getBoundingClientRect=()=>({top:1200});
  restored.window.document.dispatchEvent(new restored.window.Event('DOMContentLoaded'));
  await new Promise(resolve=>setTimeout(resolve,30));
  assert.equal(restored.window.document.querySelector('.all-lesson-questions').open,true);
  assert.equal(restored.window.__restoredY,1540);
  click(restored,'[data-action="reset"]');
  click(restored,'[data-nav="exit"]');
  assert.equal(restored.window.document.querySelector('.quiz-selection-nav').hidden,false);
  assert.equal(restored.window.document.querySelector('.quiz-navigation-controls').hidden,true);
  const emptyBook=page({book:true});
  assert.ok(emptyBook.window.document.querySelector('.quiz-selection-nav [data-mistake-link]'));
  assert.equal(emptyBook.window.document.querySelector('.quiz-selection-nav').hidden,false);
  for(const instance of [reading,reviewing,restored,emptyBook])instance.window.close();
  console.log('通过：错题标记与重做回归；浮窗入口、空错题本返回、跨页面阅读位置传递、展开状态恢复及滚动位置恢复。');
})().catch(error=>{console.error(error);process.exitCode=1;});
