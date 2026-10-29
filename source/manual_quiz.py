"""Render textbook exercises using the existing exam cards' content and rules."""
import base64
from functools import cache
import html
import json
from pathlib import Path
import re
import sqlite3
import tempfile
import zipfile

BASE = Path(__file__).resolve().parent


@cache
def card_content():
    """Read the shipped cards without running their generator or changing them."""
    cards = {}
    for group in ('法规与制度', '技术原理'):
        deck = BASE.parent / 'decks' / f'考题卡组·{group}（中译＋讲解）.apkg'
        with zipfile.ZipFile(deck) as archive, tempfile.TemporaryDirectory() as tmp:
            database = archive.extract('collection.anki2', tmp)
            with sqlite3.connect(database) as connection:
                models = json.loads(connection.execute('SELECT models FROM col').fetchone()[0])
                for model_id, fields in connection.execute('SELECT mid, flds FROM notes'):
                    names = [f['name'] for f in models[str(model_id)]['flds']]
                    values = dict(zip(names, fields.split('\x1f')))
                    cards[values['题号']] = values
    return cards


@cache
def image_data(number):
    # Embed every original image so the standalone manual also works when moved.
    image = (BASE / 'Exam1' / 'questions' / f'{number}.png').read_bytes()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('ascii')


def text_html(value):
    return html.escape(str(value), quote=False).replace('\n', '<br>')


def render_question(q, instance, stem_html=None, translation_html=None, answer_html=None):
    number = str(q['num'])
    card = card_content()[number]
    translations = re.findall(r'<span class="otr tr" hidden>(.*?)</span>', card['选项'], re.S)
    if len(translations) != len(q['propositions']):
        raise ValueError(f'Incomplete card translations: {number}')
    vocabulary = re.search(r'<table class="vtab">.*?</table>', card['选项'], re.S)
    stem_html = text_html(q['question']) if stem_html is None else stem_html
    translation_html = card['题干中译'] if translation_html is None else translation_html
    instance = html.escape(instance, quote=True)
    out = [f'<li class="exam-question" data-question="{number}" tabindex="0">',
           f'<p class="fr quiz-stem" lang="fr">{stem_html}</p>',
           f'<p class="zh quiz-tr" hidden>{translation_html}</p>',
           f'<p class="small question-number">Exam\'1 题号：{number} · 单选 '
           '<span class="quiz-selection-tag" aria-hidden="true">当前选中</span></p>',
           f'<ol class="exam-options" type="A" data-question="{number}">']
    for index, (option, translation) in enumerate(zip(q['propositions'], translations)):
        correct = ' data-ok="1"' if index == q['reponse'] else ''
        out.append('<li><button type="button" class="quiz-choice" aria-pressed="false"'
                   f'{correct}><span class="fr quiz-choice-fr" lang="fr">{text_html(option)}</span>'
                   f'<span class="quiz-tr quiz-option-tr" hidden>{translation}</span></button></li>')
    out.extend(['</ol>',
                '<div class="quiz-controls">',
                f'<button type="button" data-action="translation" aria-expanded="false" aria-controls="{instance}-translation">查看翻译（C）</button>',
                f'<button type="button" data-action="image" aria-expanded="true" aria-controls="{instance}-image">隐藏题图（X）</button>',
                '<button type="button" data-action="reset">重做本题</button>',
                '</div>',
                f'<div class="quiz-image" id="{instance}-image">',
                f'<img class="qimg" src="{image_data(number)}" alt="Exam’1 第 {number} 题原题图" loading="lazy" decoding="async">',
                '</div>',
                f'<div class="quiz-tr quiz-vocabulary" id="{instance}-translation" hidden>'])
    if vocabulary:
        out.extend(['<p class="quiz-heading">重点词汇</p>', vocabulary[0]])
    out.extend(['</div>',
                '<details class="quiz-answer"><summary>查看答案与解析（Z）</summary>'])
    if answer_html is None:
        label = chr(65 + q['reponse'])
        answer_html = (f'<p class="ans">✔ 正确答案：{label} — '
                       f'<span class="fr">{text_html(q["propositions"][q["reponse"]])}</span>'
                       f'　→　{card["答案中译"]}</p>')
    out.append(answer_html)
    if card['官方注释']:
        out.extend(['<p class="quiz-heading">题库原注</p>',
                    f'<div class="fr quiz-comment" lang="fr">{card["官方注释"]}</div>'])
    if card['注释中译']:
        out.append(f'<div class="quiz-comment-zh">{card["注释中译"]}</div>')
    if card['原理讲解']:
        out.extend(['<p class="quiz-heading">原理讲解</p>',
                    f'<div class="quiz-explanation">{card["原理讲解"]}</div>'])
    out.extend(['</details>', '</li>'])
    return '\n'.join(out)


QUIZ_CSS = """
/* Exam-card display: French and original image visible, help hidden. */
.exam-question [hidden] { display:none !important; }
.exam .exam-question { margin:1.2rem 0; padding:.3rem .2rem 1rem;
  border-bottom:1px solid #d7dfe7; position:relative; scroll-margin-top:1rem;
  border-radius:6px; transition:background-color .24s ease, box-shadow .24s ease; }
.exam .exam-question.quiz-selected { background:#edf4fb; box-shadow:0 6px 20px #28496b12; }
.quiz-selection-tag { display:inline-block; margin-left:.5rem; padding:0 .45rem;
  color:#14508c; background:#dcebf9; border-radius:4px; font-size:.8rem;
  opacity:0; transform:translateY(3px); transition:opacity .22s ease, transform .22s ease; }
.quiz-selected .quiz-selection-tag { opacity:1; transform:translateY(0); }
#quiz-selection-frame { position:absolute; top:0; left:0; pointer-events:none;
  border:2px solid #4a79a7; border-radius:8px; z-index:5; box-sizing:border-box;
  transition:transform .26s cubic-bezier(.2,.7,.2,1), width .26s ease, height .26s ease;
  box-shadow:0 0 0 3px #4a79a714; }
#quiz-selection-frame[hidden], .quiz-selection-nav[hidden] { display:none !important; }
.quiz-selection-nav { position:fixed; bottom:1rem; left:50%; transform:translateX(-50%);
  display:flex; align-items:center; gap:.5rem; padding:.5rem .7rem;
  max-width:calc(100vw - 1rem); background:#fffffff5; border:1px solid #b9c6d2;
  border-radius:10px; box-shadow:0 4px 24px #16375622; z-index:20;
  font-size:.85rem; backdrop-filter:blur(8px); }
.quiz-selection-nav button { font:inherit; cursor:pointer; padding:.35rem .5rem;
  color:#14508c; border:1px solid #cdd8e4; border-radius:4px; background:#eef3f8;
  white-space:nowrap; }
.quiz-selection-nav button:disabled { opacity:.4; cursor:default; }
.quiz-selection-status { text-align:center; min-width:8rem; line-height:1.35; }
.quiz-navigation-help { font-size:.88rem; color:#536e87; }
.exam-question:focus-visible { outline:2px solid #4a6b8a; outline-offset:4px; }
.exam .exam-options > li { padding:0; border:0; background:transparent; }
.quiz-choice { width:100%; text-align:left; font:inherit; line-height:1.5;
  color:inherit; padding:.45rem .6rem; border:1px solid #cdd8e4;
  border-radius:4px; background:#fff; cursor:pointer; overflow-wrap:anywhere; }
.quiz-choice:hover { background:#eef3f8; }
.quiz-choice:focus-visible, .quiz-controls button:focus-visible {
  outline:2px solid #14508c; outline-offset:2px; }
.quiz-choice.picked-wrong { background:#fdecea; border-color:#b3261e;
  text-decoration:line-through; }
.quiz-choice.picked-right { background:#e8f5ec; border-color:#1a6b34; font-weight:700; }
.quiz-option-tr { display:block; font-size:.86rem; color:#536e87;
  font-family:"Noto Sans CJK SC","Microsoft YaHei",sans-serif; margin-top:.2rem; }
.quiz-controls { display:flex; flex-wrap:wrap; gap:.5rem; margin:.7rem 0; }
.quiz-controls button { font:inherit; font-size:.88rem; cursor:pointer;
  color:#14508c; background:#eef3f8; border:1px solid #cdd8e4;
  border-radius:4px; padding:.3rem .6rem; }
.quiz-image { margin:.7rem 0; }
.quiz-image .qimg { display:block; max-width:100%; height:auto;
  border:1px solid #d5d5d0; border-radius:4px; background:white; }
.quiz-heading { font-weight:600; color:#14508c; margin:1rem 0 .3rem; }
.quiz-comment { color:#555; font-style:italic; }
.quiz-explanation { line-height:1.8; }
.quiz-vocabulary .vtab { font-size:.9rem; }
@media (max-width:540px) {
  .quiz-selection-nav { gap:.25rem; padding:.4rem; font-size:.75rem; }
  .quiz-selection-nav button { padding:.3rem; }
  .quiz-selection-status { min-width:0; }
}
@media (prefers-reduced-motion:reduce) {
  html { scroll-behavior:auto; }
  #quiz-selection-frame, .exam .exam-question, .quiz-selection-tag { transition:none; }
}
@media print { #quiz-selection-frame, .quiz-selection-nav { display:none !important; } }
"""

QUIZ_SCRIPT = r"""
(function () {
  'use strict';
  if (window.__manualQuizBound) return;
  window.__manualQuizBound = true;
  var active = null;
  var questions = Array.from(document.querySelectorAll('.exam-question'));
  if (!questions.length) return;
  questions.forEach(function (question, index) { question.tabIndex = index === 0 ? 0 : -1; });
  var frame = document.createElement('div');
  frame.id = 'quiz-selection-frame';
  frame.hidden = true;
  frame.setAttribute('aria-hidden', 'true');
  document.body.appendChild(frame);
  var navigation = document.createElement('nav');
  navigation.className = 'quiz-selection-nav';
  navigation.setAttribute('aria-label', '课后例题选题');
  navigation.hidden = true;
  navigation.innerHTML = '<button type="button" data-nav="previous" aria-label="上一道题（上方向键）">↑ 上一题</button>' +
    '<span class="quiz-selection-status" aria-live="polite"></span>' +
    '<button type="button" data-nav="next" aria-label="下一道题（下方向键）">下一题 ↓</button>' +
    '<button type="button" data-nav="exit" aria-label="退出选题（Escape）">退出</button>';
  document.body.appendChild(navigation);
  var scheduled = false;
  function moveFrame() {
    if (!active) return;
    var rect = active.getBoundingClientRect();
    frame.style.width = (rect.width + 12) + 'px';
    frame.style.height = (rect.height + 8) + 'px';
    frame.style.transform = 'translate3d(' + (rect.left + window.scrollX - 6) + 'px,' +
      (rect.top + window.scrollY - 4) + 'px,0)';
  }
  function scheduleFrame() {
    if (scheduled) return;
    scheduled = true;
    window.requestAnimationFrame(function () { scheduled = false; moveFrame(); });
  }
  function select(question, scroll) {
    if (!question) return;
    if (active !== question) {
      if (active) {
        active.classList.remove('quiz-selected');
        active.removeAttribute('aria-current');
        active.tabIndex = -1;
      }
      active = question;
      active.classList.add('quiz-selected');
      active.setAttribute('aria-current', 'true');
      active.tabIndex = 0;
    }
    var index = questions.indexOf(active);
    navigation.querySelector('.quiz-selection-status').textContent =
      '第 ' + (index + 1) + ' / ' + questions.length + ' 题 · ' + active.getAttribute('data-question');
    navigation.querySelector('[data-nav="previous"]').disabled = index === 0;
    navigation.querySelector('[data-nav="next"]').disabled = index === questions.length - 1;
    navigation.hidden = false;
    moveFrame();
    frame.hidden = false;
    if (scroll) {
      active.focus({ preventScroll:true });
      active.scrollIntoView({ behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block:'start' });
    }
  }
  function step(direction) {
    if (!active) return;
    var index = questions.indexOf(active) + direction;
    if (index >= 0 && index < questions.length) select(questions[index], true);
  }
  function exit() {
    if (active) {
      active.classList.remove('quiz-selected');
      active.removeAttribute('aria-current');
    }
    active = null;
    frame.hidden = true;
    navigation.hidden = true;
  }
  function questionFor(target) {
    return target && target.closest ? target.closest('.exam-question') : null;
  }
  function translations(question, on) {
    question.querySelectorAll('.quiz-tr').forEach(function (element) { element.hidden = !on; });
    var button = question.querySelector('[data-action="translation"]');
    button.textContent = on ? '隐藏翻译（C）' : '查看翻译（C）';
    button.setAttribute('aria-expanded', String(on));
    scheduleFrame();
  }
  function image(question, on) {
    question.querySelector('.quiz-image').hidden = !on;
    var button = question.querySelector('[data-action="image"]');
    button.textContent = on ? '隐藏题图（X）' : '查看题图（X）';
    button.setAttribute('aria-expanded', String(on));
    scheduleFrame();
  }
  function choose(question, button) {
    if (button.classList.contains('picked-right')) return;
    var correct = button.getAttribute('data-ok') === '1';
    button.classList.add(correct ? 'picked-right' : 'picked-wrong');
    button.setAttribute('aria-pressed', 'true');
    scheduleFrame();
  }
  function reset(question) {
    question.querySelectorAll('.quiz-choice').forEach(function (button) {
      button.classList.remove('picked-right', 'picked-wrong');
      button.setAttribute('aria-pressed', 'false');
    });
    translations(question, false);
    image(question, true);
    question.querySelector('.quiz-answer').open = false;
  }
  document.addEventListener('focusin', function (event) {
    var question = questionFor(event.target);
    if (question) select(question, false);
  });
  document.addEventListener('click', function (event) {
    var navButton = event.target.closest('[data-nav]');
    if (navButton && navigation.contains(navButton)) {
      var direction = navButton.getAttribute('data-nav');
      if (direction === 'exit') exit();
      else step(direction === 'previous' ? -1 : 1);
      return;
    }
    var question = questionFor(event.target);
    if (!question) return;
    select(question, false);
    var button = event.target.closest('button');
    if (!button) {
      if (!event.target.closest('a, summary, input, textarea, select')) active.focus({ preventScroll:true });
      return;
    }
    if (button.classList.contains('quiz-choice')) { choose(active, button); return; }
    var action = button.getAttribute('data-action');
    if (action === 'translation') translations(active, button.getAttribute('aria-expanded') !== 'true');
    else if (action === 'image') image(active, active.querySelector('.quiz-image').hidden);
    else if (action === 'reset') reset(active);
  });
  document.addEventListener('keydown', function (event) {
    if (!active || event.ctrlKey || event.metaKey || event.altKey || event.isComposing || event.repeat) return;
    var target = event.target;
    if (target && (target.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(target.tagName))) return;
    var key = event.key.toLowerCase();
    if (key === 'arrowdown' || key === 'arrowright') {
      step(1);
    } else if (key === 'arrowup' || key === 'arrowleft') {
      step(-1);
    } else if (key === 'escape') {
      exit();
    } else if (/^[1-4]$/.test(key)) {
      var button = active.querySelectorAll('.quiz-choice')[Number(key) - 1];
      if (button) choose(active, button);
    } else if (key === 'c') {
      translations(active, active.querySelector('[data-action="translation"]').getAttribute('aria-expanded') !== 'true');
    } else if (key === 'x') {
      image(active, active.querySelector('.quiz-image').hidden);
    } else if (key === 'z') {
      var answer = active.querySelector('.quiz-answer');
      answer.open = !answer.open;
    } else return;
    event.preventDefault();
    scheduleFrame();
  });
  document.addEventListener('toggle', scheduleFrame, true);
  document.addEventListener('load', scheduleFrame, true);
  window.addEventListener('resize', scheduleFrame);
  if (window.ResizeObserver) {
    var observer = new window.ResizeObserver(scheduleFrame);
    observer.observe(document.querySelector('main') || document.body);
    questions.forEach(function (question) { observer.observe(question); });
  }
})();
"""
