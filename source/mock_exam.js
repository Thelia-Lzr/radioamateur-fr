(function () {
  'use strict';
  var data = JSON.parse(document.getElementById('mock-exam-data').textContent);
  var storageKey = 'radioamateur-fr.mock-exam.v1';
  var bank = new Map();
  document.getElementById('mock-exam-bank').content.querySelectorAll('.exam-question').forEach(function (node) {
    bank.set(node.getAttribute('data-question'), node);
  });
  var metadata = new Map(data.questions.map(function (q) { return [q.id, q]; }));
  var state = null;
  var interval = null;
  function node(id) { return document.getElementById(id); }
  function message(text) { node('exam-message').textContent = text; }
  function format(seconds) {
    seconds = Math.max(0, Math.floor(seconds));
    return String(Math.floor(seconds / 60)).padStart(2, '0') + ':' + String(seconds % 60).padStart(2, '0');
  }
  function save() {
    try {
      if (state) localStorage.setItem(storageKey, JSON.stringify(state));
      else localStorage.removeItem(storageKey);
    } catch (error) { node('exam-storage-notice').hidden = false; }
  }
  function valid(value) {
    if (!value || value.version !== data.version || !data.modes[value.kind] ||
        !['running', 'submitted'].includes(value.status) ||
        !Array.isArray(value.ids) || value.ids.length !== 20 || new Set(value.ids).size !== 20 ||
        !Array.isArray(value.answers) || value.answers.length !== 20 ||
        !value.answers.every(function (answer) { return Number.isInteger(answer) && answer >= -1 && answer <= 3; }) ||
        !Number.isInteger(value.current) || value.current < 0 || value.current >= 20 ||
        !Number.isFinite(value.startedAt) || value.startedAt <= 0 ||
        value.deadline !== value.startedAt + data.modes[value.kind].seconds * 1000) return false;
    if (value.status === 'submitted' && (!Number.isFinite(value.finishedAt) || value.finishedAt < value.startedAt ||
        value.finishedAt > value.deadline || !['manual', 'timeout'].includes(value.reason))) return false;
    var themeCounts = new Map();
    var chapters = new Set();
    for (var id of value.ids) {
      var q = metadata.get(id);
      if (!q || !bank.has(id) || q.kind !== value.kind) return false;
      themeCounts.set(q.theme, (themeCounts.get(q.theme) || 0) + 1);
      chapters.add(q.chapter);
    }
    return data.modes[value.kind].themes.every(function (theme) { return themeCounts.get(theme) === 2; }) &&
      data.modes[value.kind].chapters.every(function (chapter) { return chapters.has(chapter); });
  }
  function panels(panel) {
    ['exam-setup', 'exam-running', 'exam-results'].forEach(function (id) { node(id).hidden = id !== panel; });
  }
  function stopTimer() { if (interval !== null) window.clearInterval(interval); interval = null; }
  function typeset(target) {
    if (window.MathJax && window.MathJax.typesetPromise) window.MathJax.typesetPromise([target]).catch(function () {});
  }
  function updateProgress() {
    var answered = state.answers.filter(function (answer) { return answer !== -1; }).length;
    node('exam-progress').textContent = '已答 ' + answered + ' / 20';
    node('exam-question-map').querySelectorAll('button').forEach(function (button, index) {
      button.classList.toggle('exam-map-answered', state.answers[index] !== -1);
      if (index === state.current) button.setAttribute('aria-current', 'step');
      else button.removeAttribute('aria-current');
      button.setAttribute('aria-label', '第 ' + (index + 1) + ' 题，' + (state.answers[index] === -1 ? '未答' : '已答'));
    });
    var recap = node('exam-recap-body');
    recap.replaceChildren();
    state.answers.forEach(function (answer, index) {
      var row = document.createElement('tr');
      var number = document.createElement('td');
      var button = document.createElement('button');
      button.type = 'button'; button.setAttribute('data-exam-jump', String(index)); button.textContent = '第 ' + (index + 1) + ' 题';
      number.appendChild(button);
      var choice = document.createElement('td');
      choice.textContent = answer === -1 ? '未作答' : String.fromCharCode(65 + answer);
      row.append(number, choice); recap.appendChild(row);
    });
    node('exam-clear').disabled = state.answers[state.current] === -1;
    node('exam-previous').disabled = state.current === 0;
    node('exam-next').disabled = state.current === 19;
  }
  function paintChoices() {
    node('exam-question-host').querySelectorAll('.quiz-choice').forEach(function (button, index) {
      var selected = state.answers[state.current] === index;
      button.classList.toggle('exam-choice-selected', selected);
      button.setAttribute('aria-pressed', String(selected));
    });
    updateProgress();
  }
  function showQuestion(focus) {
    var host = node('exam-question-host');
    if (window.MathJax && window.MathJax.typesetClear) window.MathJax.typesetClear([host]);
    var question = bank.get(state.ids[state.current]).cloneNode(true);
    question.removeAttribute('tabindex');
    question.querySelectorAll('.quiz-tr, .quiz-controls, .quiz-answer, .quiz-selection-tag').forEach(function (element) { element.remove(); });
    question.querySelector('.question-number').textContent = '第 ' + (state.current + 1) + ' / 20 题';
    question.querySelectorAll('.quiz-choice').forEach(function (button, index) {
      button.removeAttribute('data-ok');
      button.setAttribute('data-exam-option', String(index));
      button.setAttribute('aria-pressed', 'false');
    });
    var heading = document.createElement('h2');
    heading.className = 'exam-question-heading';
    heading.textContent = '第 ' + (state.current + 1) + ' 题';
    heading.tabIndex = -1;
    var list = document.createElement('ol');
    list.appendChild(question);
    host.replaceChildren(heading, list);
    paintChoices(); typeset(host);
    if (focus) heading.focus({preventScroll:false});
  }
  function reviewFilter(filter) {
    var visible = 0;
    Array.from(node('exam-review-list').children).forEach(function (question) {
      var right = question.getAttribute('data-exam-result') === 'right';
      question.hidden = filter === 'wrong' ? right : filter === 'right' ? !right : false;
      if (!question.hidden) visible++;
    });
    node('exam-review-empty').hidden = visible > 0;
    node('exam-review-filters').querySelectorAll('[data-exam-filter]').forEach(function (button) {
      button.setAttribute('aria-pressed', String(button.getAttribute('data-exam-filter') === filter));
    });
  }
  function results(focus) {
    panels('exam-results');
    node('exam-submit-check').hidden = true;
    var rightCount = 0;
    var blankCount = 0;
    var reviewList = node('exam-review-list');
    reviewList.replaceChildren();
    state.ids.forEach(function (id, index) {
      var info = metadata.get(id);
      var answer = state.answers[index];
      var right = answer === info.answer;
      if (right) rightCount++;
      if (answer === -1) blankCount++;
      var question = bank.get(id).cloneNode(true);
      question.classList.add('exam-review-card');
      question.setAttribute('data-exam-result', right ? 'right' : answer === -1 ? 'blank' : 'wrong');
      question.querySelectorAll('.quiz-selection-tag, [data-action="reset"]').forEach(function (element) { element.remove(); });
      question.querySelectorAll('.quiz-choice').forEach(function (button, option) {
        button.disabled = true;
        button.classList.toggle('picked-right', option === info.answer);
        button.classList.toggle('picked-wrong', option === answer && !right);
        button.setAttribute('aria-pressed', String(option === answer));
      });
      var heading = document.createElement('h3');
      heading.className = 'exam-review-result';
      heading.textContent = '第 ' + (index + 1) + ' 题 · ' + (right ? '答对' : answer === -1 ? '未答' : '答错');
      var summary = document.createElement('p');
      summary.className = 'small';
      summary.textContent = '你的答案：' + (answer === -1 ? '未作答' : String.fromCharCode(65 + answer)) +
        '；正确答案：' + String.fromCharCode(65 + info.answer) + '。考点：' + data.themes[String(info.theme)] + '（' + info.section + '）';
      question.prepend(heading, summary);
      question.querySelectorAll('.quiz-tr').forEach(function (element) { element.hidden = false; });
      var translation = question.querySelector('[data-action="translation"]');
      translation.textContent = '隐藏翻译与词汇'; translation.setAttribute('aria-expanded', 'true');
      var image = question.querySelector('[data-action="image"]');
      image.textContent = '隐藏题图';
      question.querySelector('.quiz-answer').open = true;
      question.querySelector('.quiz-answer > summary').textContent = '答案与解析';
      reviewList.appendChild(question);
    });
    var mode = data.modes[state.kind];
    var score = node('exam-score');
    var title = document.createElement('h2');
    title.textContent = mode.label + '：' + rightCount + ' / 20 · ' + (rightCount >= 10 ? '及格' : '未及格');
    var totals = document.createElement('p');
    totals.textContent = '答对 ' + rightCount + ' 题 · 答错 ' + (20 - rightCount - blankCount) + ' 题 · 未答 ' + blankCount + ' 题';
    var timing = document.createElement('p');
    timing.textContent = (state.reason === 'timeout' ? '时间到，已自动交卷。' : '已提交试卷。') + '用时 ' +
      format((state.finishedAt - state.startedAt) / 1000) + ' / ' + format(mode.seconds) + '；及格线 10/20。';
    score.replaceChildren(title, totals, timing);
    score.classList.toggle('exam-passed', rightCount >= 10);
    score.classList.toggle('exam-failed', rightCount < 10);
    node('exam-coverage').textContent = '本卷覆盖 10 类知识点（各 2 题）、' + mode.chapters.length + ' 个大章、' +
      new Set(state.ids.map(function (id) { return metadata.get(id).section; })).size + ' 个小节。';
    var themeScores = node('exam-theme-scores');
    themeScores.replaceChildren();
    mode.themes.forEach(function (theme) {
      var correct = 0;
      var unanswered = 0;
      state.ids.forEach(function (id, index) {
        var info = metadata.get(id);
        if (info.theme !== theme) return;
        if (state.answers[index] === info.answer) correct++;
        if (state.answers[index] === -1) unanswered++;
      });
      var row = document.createElement('tr');
      [data.themes[String(theme)], correct + ' / 2', String(unanswered)].forEach(function (text) {
        var cell = document.createElement('td'); cell.textContent = text; row.appendChild(cell);
      });
      themeScores.appendChild(row);
    });
    node('exam-review-filters').querySelector('[data-exam-filter="all"]').textContent = '全部（20）';
    node('exam-review-filters').querySelector('[data-exam-filter="wrong"]').textContent = '错题／未答（' + (20 - rightCount) + '）';
    node('exam-review-filters').querySelector('[data-exam-filter="right"]').textContent = '对题（' + rightCount + '）';
    reviewFilter('all');
    if (window.radioMistakes) window.radioMistakes.sync();
    typeset(reviewList);
    if (focus) score.focus({preventScroll:false});
  }
  function finish(reason) {
    if (!state || state.status !== 'running') return;
    var now = Date.now();
    state.status = 'submitted';
    state.reason = now >= state.deadline ? 'timeout' : reason;
    state.finishedAt = Math.max(state.startedAt, Math.min(now, state.deadline));
    stopTimer(); save(); results(true);
    message(state.reason === 'timeout' ? '考试时间到，试卷已自动提交。' : '试卷已提交，可以查看全部题目的答案与解析。');
  }
  function tick() {
    if (!state || state.status !== 'running') return false;
    var now = Date.now();
    var remaining = Math.max(0, state.deadline - now);
    node('exam-remaining').textContent = format(Math.ceil(remaining / 1000));
    node('exam-time-progress').value = Math.ceil(remaining / 1000);
    node('exam-elapsed').textContent = format(Math.min(data.modes[state.kind].seconds, Math.max(0, now - state.startedAt) / 1000));
    node('exam-remaining').closest('.exam-session-toolbar').classList.toggle('exam-time-low', remaining <= 60000);
    if (remaining === 0) { finish('timeout'); return false; }
    return true;
  }
  function running() {
    panels('exam-running');
    node('exam-submit-check').hidden = true;
    node('exam-mode-label').textContent = data.modes[state.kind].label + '模拟考试';
    node('exam-time-progress').max = data.modes[state.kind].seconds;
    var navigation = node('exam-question-map');
    navigation.replaceChildren();
    state.ids.forEach(function (id, index) {
      var button = document.createElement('button');
      button.type = 'button'; button.textContent = String(index + 1);
      button.setAttribute('data-exam-jump', String(index)); navigation.appendChild(button);
    });
    showQuestion(false);
    stopTimer();
    if (tick()) interval = window.setInterval(tick, 1000);
  }
  function start(kind) {
    var mode = data.modes[kind];
    if (!mode || (state && state.status === 'running')) return;
    try {
      var questions = data.questions.filter(function (q) { return q.kind === kind && bank.has(q.id); });
      var drawn = window.radioExamSampling.draw(questions, mode.themes, mode.chapters);
      var now = Date.now();
      state = {version:data.version, kind:kind, status:'running', ids:drawn.map(function (q) { return q.id; }),
        answers:new Array(20).fill(-1), current:0, startedAt:now, deadline:now + mode.seconds * 1000};
      save(); message('考试已开始，倒计时持续运行。'); running();
    } catch (error) { message('无法生成试卷：' + error.message); }
  }
  function move(index) {
    if (!tick() || index < 0 || index >= 20) return;
    state.current = index; save(); showQuestion(true);
  }
  function choose(answer) {
    if (!tick()) return;
    state.answers[state.current] = answer; save(); paintChoices();
  }
  function confirmSubmission() {
    if (!tick()) return;
    var blanks = state.answers.filter(function (answer) { return answer === -1; }).length;
    node('exam-submit-summary').textContent = '已答 ' + (20 - blanks) + ' / 20 题' +
      (blanks ? '，还有 ' + blanks + ' 题未作答' : '') + '。提交后结束计时并查看结果。';
    node('exam-submit-check').hidden = false;
    node('exam-confirm-submit').focus();
  }
  document.addEventListener('click', function (event) {
    var button = event.target.closest('button');
    if (!button) return;
    if (button.hasAttribute('data-exam-start')) { start(button.getAttribute('data-exam-start')); return; }
    if (button.hasAttribute('data-exam-jump')) { move(Number(button.getAttribute('data-exam-jump'))); return; }
    if (button.hasAttribute('data-exam-option')) { choose(Number(button.getAttribute('data-exam-option'))); return; }
    if (button.hasAttribute('data-exam-submit')) { confirmSubmission(); return; }
    if (button.hasAttribute('data-exam-filter')) { reviewFilter(button.getAttribute('data-exam-filter')); return; }
    if (button.id === 'exam-previous') move(state.current - 1);
    else if (button.id === 'exam-next') move(state.current + 1);
    else if (button.id === 'exam-clear') choose(-1);
    else if (button.id === 'exam-confirm-submit') finish('manual');
    else if (button.id === 'exam-continue') { node('exam-submit-check').hidden = true; showQuestion(true); }
    else if (button.id === 'exam-restart') start(state.kind);
    else if (button.id === 'exam-change-mode') { stopTimer(); state = null; save(); panels('exam-setup'); message('请选择法规或技术考试。'); }
    else if (state && state.status === 'submitted') {
      var question = button.closest('.exam-review-card');
      if (!question) return;
      if (button.getAttribute('data-action') === 'translation') {
        var on = button.getAttribute('aria-expanded') !== 'true';
        question.querySelectorAll('.quiz-tr').forEach(function (element) { element.hidden = !on; });
        button.setAttribute('aria-expanded', String(on)); button.textContent = on ? '隐藏翻译与词汇' : '查看翻译与词汇';
      } else if (button.getAttribute('data-action') === 'image') {
        var image = question.querySelector('.quiz-image'); image.hidden = !image.hidden;
        button.setAttribute('aria-expanded', String(!image.hidden)); button.textContent = image.hidden ? '查看题图' : '隐藏题图';
      }
    }
  });
  document.addEventListener('keydown', function (event) {
    if (!state || state.status !== 'running' || event.ctrlKey || event.metaKey || event.altKey || event.repeat || event.isComposing ||
        !node('exam-submit-check').hidden || event.target.closest('#study-sidebar, [data-sidebar-toggle], input, textarea, select, [contenteditable]')) return;
    if (/^[1-4]$/.test(event.key)) choose(Number(event.key) - 1);
    else if (event.key === 'ArrowLeft') move(state.current - 1);
    else if (event.key === 'ArrowRight') move(state.current + 1);
    else return;
    event.preventDefault();
  });
  document.addEventListener('visibilitychange', tick);
  window.addEventListener('pageshow', tick);
  window.addEventListener('pagehide', function () { tick(); save(); });
  try {
    var restored = JSON.parse(localStorage.getItem(storageKey) || 'null');
    if (valid(restored)) state = restored;
    else if (restored) { localStorage.removeItem(storageKey); message('旧考试记录不完整，请重新选择科目开始。'); }
  } catch (error) { node('exam-storage-notice').hidden = false; }
  if (state && state.status === 'running') { message('已恢复作答进度，倒计时继续运行。'); running(); }
  else if (state) results(false);
})();
