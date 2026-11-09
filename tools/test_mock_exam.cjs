/* NODE_PATH=/path/to/node_modules node tools/test_mock_exam.cjs */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {JSDOM} = require('jsdom');
const root = path.join(__dirname, '..');
const page = fs.readFileSync(path.join(root, 'mock-exam.html'), 'utf8');
const data = JSON.parse(page.match(/<script id="mock-exam-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const metadata = new Map(data.questions.map(q=>[q.id,q]));
const sampling = fs.readFileSync(path.join(root, 'source/mock_exam_sampling.js'), 'utf8');
const application = fs.readFileSync(path.join(root, 'source/mock_exam.js'), 'utf8');
const mistakes = fs.readFileSync(path.join(root, 'source/quiz_mistakes.js'), 'utf8');
const navigation = fs.readFileSync(path.join(root, 'source/study_navigation.js'), 'utf8');
require(path.join(root, 'source/mock_exam_sampling.js'));
function random(seed) {
  return () => { seed=(Math.imul(seed,1664525)+1013904223)>>>0; return seed/4294967296; };
}
const fixtureIds = new Set();
for (const [kind, mode] of Object.entries(data.modes)) {
  const questions=data.questions.filter(q=>q.kind===kind);
  const signatures=new Set();
  for (let seed=1; seed<=500; seed++) {
    const drawn=globalThis.radioExamSampling.draw(questions,mode.themes,mode.chapters,random(seed));
    assert.equal(drawn.length,20);
    assert.equal(new Set(drawn.map(q=>q.id)).size,20);
    assert.ok(drawn.every(q=>q.kind===kind));
    for (const theme of mode.themes) assert.equal(drawn.filter(q=>q.theme===theme).length,2);
    for (const chapter of mode.chapters) assert.ok(drawn.some(q=>q.chapter===chapter),chapter);
    signatures.add(drawn.map(q=>q.id).sort().join(','));
    if(seed===1) drawn.forEach(q=>fixtureIds.add(q.id));
  }
  assert.ok(signatures.size>490,'new exams should draw different questions');
}
assert.throws(()=>globalThis.radioExamSampling.draw([],data.modes.regulation.themes,[],random(1)),/题量不足/);
const templates=Array.from(page.matchAll(/<li class="exam-question"[^>]*>.*?<\/details>\s*<\/li>/gs));
assert.equal(templates.length,2688);
const samples=templates.filter(match=>fixtureIds.has(match[0].match(/data-question="(\d+)"/)[1]))
  .map(match=>match[0].replace(/data:image\/png;base64,[^"]+/g,''));
const markup=page.slice(page.indexOf('<body'),page.indexOf('<template id="mock-exam-bank">'));
const storageKey='radioamateur-fr.mock-exam.v1';
const instances=[];
function fixture({saved=null,wall={now:1794150000000},blocked=false,hash=''}={}) {
  const dom=new JSDOM(markup+'<template id="mock-exam-bank"><ol>'+samples.join('')+'</ol></template>'+
    '<script id="mock-exam-data" type="application/json">'+JSON.stringify(data)+'</script>',
    {url:'https://offline.test/mock-exam.html'+hash,runScripts:'outside-only',pretendToBeVisual:true});
  instances.push(dom);
  const win=dom.window;
  win.Date.now=()=>wall.now;
  win.matchMedia=()=>({matches:false,addEventListener(){}});
  win.scrollTo=()=>{};
  if(saved!==null)win.localStorage.setItem(storageKey,saved);
  if(blocked)Object.defineProperty(win,'localStorage',{get(){throw Error('storage blocked');}});
  win.eval(mistakes); win.eval(navigation); win.eval(sampling); win.eval(application);
  return dom;
}
function click(dom,selector) { const target=dom.window.document.querySelector(selector); assert.ok(target,selector); target.click(); }
function stored(dom) { return JSON.parse(dom.window.localStorage.getItem(storageKey)); }
function tick(dom) { dom.window.document.dispatchEvent(new dom.window.Event('visibilitychange')); }
function visibleResults(dom) { return Array.from(dom.window.document.querySelectorAll('.exam-review-card')).filter(q=>!q.hidden); }
try {
  const wall={now:1794150000000};
  const returnPoint={anchor:'R45',offset:24};
  const dom=fixture({wall,hash:'#marks=%5B%5D&return='+encodeURIComponent(JSON.stringify(returnPoint))});
  const doc=dom.window.document;
  assert.equal(doc.querySelector('.sidebar-shortcuts').children[2].textContent,'模拟考试');
  assert.equal(doc.querySelector('.sidebar-shortcuts').children[2].getAttribute('aria-current'),'page');
  click(dom,'[data-exam-start="regulation"]');
  assert.equal(doc.getElementById('exam-setup').hidden,true);
  assert.equal(doc.getElementById('exam-remaining').textContent,'15:00');
  assert.equal(doc.getElementById('exam-elapsed').textContent,'00:00');
  assert.equal(stored(dom).deadline-stored(dom).startedAt,900000);
  assert.equal(doc.querySelectorAll('#exam-question-map button').length,20);
  assert.equal(doc.querySelectorAll('#exam-recap-body tr').length,20);
  assert.equal(doc.querySelectorAll('#exam-question-host .quiz-choice').length,4);
  assert.equal(doc.querySelectorAll('#exam-question-host .quiz-tr, #exam-question-host .quiz-answer, #exam-question-host [data-ok]').length,0);
  click(dom,'[data-exam-option="0"]');
  click(dom,'[data-exam-option="1"]');
  assert.equal(stored(dom).answers[0],1);
  assert.equal(doc.querySelectorAll('#exam-question-host [aria-pressed="true"]').length,1);
  assert.equal(doc.querySelector('#exam-recap-body tr').children[1].textContent,'B');
  assert.equal(doc.querySelectorAll('#exam-question-host .picked-right, #exam-question-host .picked-wrong').length,0);
  click(dom,'#exam-clear');
  assert.equal(stored(dom).answers[0],-1);
  wall.now+=55400;tick(dom);
  assert.equal(doc.getElementById('exam-remaining').textContent,'14:05');
  assert.equal(doc.getElementById('exam-elapsed').textContent,'00:55');
  assert.equal(doc.getElementById('exam-time-progress').value,845);
  for(let i=0;i<15;i++) {
    click(dom,'#exam-question-map [data-exam-jump="'+i+'"]');
    const correct=metadata.get(stored(dom).ids[i]).answer;
    click(dom,'[data-exam-option="'+(i<10?correct:(correct+1)%4)+'"]');
  }
  assert.equal(doc.getElementById('exam-progress').textContent,'已答 15 / 20');
  click(dom,'[data-exam-submit]');
  assert.equal(doc.getElementById('exam-submit-check').hidden,false);
  assert.match(doc.getElementById('exam-submit-summary').textContent,/5 题未作答/);
  click(dom,'#exam-continue');
  assert.equal(doc.getElementById('exam-submit-check').hidden,true);
  wall.now+=39600;
  click(dom,'[data-exam-submit]');click(dom,'#exam-confirm-submit');
  assert.equal(stored(dom).status,'submitted');
  assert.equal(stored(dom).finishedAt-stored(dom).startedAt,95000);
  assert.match(doc.getElementById('exam-score').textContent,/10 \/ 20 · 及格/);
  assert.match(doc.getElementById('exam-score').textContent,/答对 10 题 · 答错 5 题 · 未答 5 题/);
  assert.match(doc.getElementById('exam-score').textContent,/01:35/);
  assert.equal(doc.querySelectorAll('.exam-review-card').length,20);
  assert.equal(doc.querySelectorAll('.exam-review-card .quiz-answer[open]').length,20);
  assert.equal(doc.querySelectorAll('.exam-review-card .quiz-choice:disabled').length,80);
  assert.equal(doc.querySelectorAll('.exam-review-card .picked-right').length,20);
  assert.equal(doc.querySelectorAll('.exam-review-card .picked-wrong').length,5);
  assert.equal(doc.querySelectorAll('#exam-theme-scores tr').length,10);
  assert.equal(Array.from(doc.querySelectorAll('#exam-theme-scores tr')).reduce((sum,row)=>sum+Number(row.children[1].textContent.split('/')[0]),0),10);
  click(dom,'[data-exam-filter="wrong"]');
  assert.equal(visibleResults(dom).length,10);
  assert.ok(visibleResults(dom).some(q=>q.dataset.examResult==='blank'));
  click(dom,'[data-exam-filter="right"]');assert.equal(visibleResults(dom).length,10);
  click(dom,'[data-exam-filter="all"]');assert.equal(visibleResults(dom).length,20);
  const wrong=doc.querySelector('.exam-review-card[data-exam-result="wrong"]');
  wrong.querySelector('[data-action="mistake"]').click();
  const bookUrl=new URL(doc.querySelector('[data-mistake-link="mistake-book.html"]').href);
  const params=new URLSearchParams(bookUrl.hash.slice(1));
  assert.ok(JSON.parse(params.get('marks')).includes(wrong.dataset.question));
  assert.deepEqual(JSON.parse(params.get('return')),returnPoint);
  const grade=stored(dom);
  wall.now+=5000000;tick(dom);
  assert.deepEqual(stored(dom),grade,'submitted results must stay immutable');
  const restoredResult=fixture({saved:JSON.stringify(grade),wall});
  assert.match(restoredResult.window.document.getElementById('exam-score').textContent,/10 \/ 20/);
  click(dom,'#exam-change-mode');
  assert.equal(doc.getElementById('exam-setup').hidden,false);
  assert.equal(stored(dom),null);
  const techWall={now:1794150000000};
  const tech=fixture({wall:techWall});
  click(tech,'[data-exam-start="technique"]');
  assert.equal(tech.window.document.getElementById('exam-remaining').textContent,'30:00');
  assert.equal(tech.window.document.getElementById('exam-time-progress').max,1800);
  click(tech,'[data-exam-option="3"]');
  techWall.now+=123000;tick(tech);
  const runningRecord=stored(tech);
  techWall.now+=600000;
  const resumed=fixture({saved:JSON.stringify(runningRecord),wall:techWall});
  assert.equal(resumed.window.document.getElementById('exam-remaining').textContent,'17:57');
  assert.equal(resumed.window.document.getElementById('exam-elapsed').textContent,'12:03');
  assert.equal(stored(resumed).answers[0],3);
  assert.equal(resumed.window.document.querySelector('[data-exam-option="3"]').getAttribute('aria-pressed'),'true');
  const beforeExpiry=stored(resumed);
  techWall.now=beforeExpiry.deadline+5000;
  click(resumed,'[data-exam-option="1"]');
  assert.equal(stored(resumed).status,'submitted');
  assert.equal(stored(resumed).reason,'timeout');
  assert.equal(stored(resumed).finishedAt,beforeExpiry.deadline);
  assert.deepEqual(stored(resumed).answers,beforeExpiry.answers,'a late answer must not be counted');
  assert.match(resumed.window.document.getElementById('exam-score').textContent,/时间到，已自动交卷/);
  assert.match(resumed.window.document.getElementById('exam-score').textContent,/30:00 \/ 30:00/);
  const alreadyExpired=fixture({saved:JSON.stringify(runningRecord),wall:techWall});
  assert.equal(stored(alreadyExpired).reason,'timeout');
  const invalid=fixture({saved:JSON.stringify({...runningRecord,ids:new Array(20).fill(runningRecord.ids[0])})});
  assert.equal(invalid.window.document.getElementById('exam-setup').hidden,false);
  assert.equal(stored(invalid),null);
  const blocked=fixture({blocked:true});
  click(blocked,'[data-exam-start="regulation"]');
  assert.equal(blocked.window.document.getElementById('exam-running').hidden,false);
  assert.equal(blocked.window.document.getElementById('exam-storage-notice').hidden,false);
  click(blocked,'[data-exam-option="0"]');
  assert.equal(blocked.window.document.querySelector('[data-exam-option="0"]').getAttribute('aria-pressed'),'true');
  console.log('通过：1000 次随机组卷的主题／章节覆盖与无重复；法规／技术时限、单选修改、答题总览、计分、解析筛选、刷新恢复、超时拒绝迟答及错题标记传递。');
} finally { instances.forEach(dom=>dom.window.close()); }
