(function () {
  'use strict';
  var storageKey = 'radioamateur-fr.mistakes.v1';
  var marked = [];
  var storageAvailable = true;
  function clean(value) {
    if (!Array.isArray(value)) return [];
    return Array.from(new Set(value.filter(function (n) { return typeof n === 'string' && /^\d{5}$/.test(n); }))).sort();
  }
  function read() {
    try { return clean(JSON.parse(localStorage.getItem(storageKey) || '[]')); }
    catch (error) { storageAvailable = false; return []; }
  }
  function save() {
    try { localStorage.setItem(storageKey, JSON.stringify(marked)); }
    catch (error) { storageAvailable = false; }
  }
  marked = read();
  // A full snapshot in navigation links also works when file:// pages have separate storage.
  if (location.hash.indexOf('#marks=') === 0) {
    try {
      var incoming = JSON.parse(decodeURIComponent(location.hash.slice(7)));
      if (Array.isArray(incoming)) { marked = clean(incoming); save(); }
    } catch (error) { /* Keep saved marks if a link is malformed. */ }
    try { history.replaceState(null, '', location.pathname + location.search); } catch (error) {}
  }
  function sync() {
    document.querySelectorAll('[data-action="mistake"]').forEach(function (button) {
      var question = button.closest('.exam-question');
      var on = marked.indexOf(question.getAttribute('data-question')) !== -1;
      button.setAttribute('aria-pressed', String(on));
      button.textContent = on ? '移出错题本' : '标记错题';
      question.classList.toggle('quiz-marked', on);
    });
    document.querySelectorAll('[data-mistake-count]').forEach(function (node) { node.textContent = marked.length; });
    document.querySelectorAll('[data-mistake-link]').forEach(function (link) {
      link.href = link.getAttribute('data-mistake-link') + '#marks=' + encodeURIComponent(JSON.stringify(marked));
    });
    document.querySelectorAll('[data-mistake-storage]').forEach(function (node) { node.hidden = storageAvailable; });
  }
  function toggle(number) {
    // Re-read shared storage to avoid overwriting marks made in another open tab.
    if (storageAvailable) marked = read();
    var index = marked.indexOf(number);
    if (index === -1) marked.push(number); else marked.splice(index, 1);
    marked = clean(marked); save(); sync();
  }
  window.radioMistakes = { numbers:function () { return marked.slice(); }, sync:sync };
  document.addEventListener('click', function (event) {
    var button = event.target.closest('[data-action="mistake"]');
    if (button) toggle(button.closest('.exam-question').getAttribute('data-question'));
    var link = event.target.closest('[data-mistake-link]');
    if (link) sync();
  });
  window.addEventListener('storage', function (event) {
    if (event.key === storageKey || event.key === null) { marked = read(); sync(); }
  });
  if (document.body.hasAttribute('data-mistake-book')) {
    var bank = document.getElementById('mistake-bank');
    var list = document.getElementById('mistake-questions');
    var wanted = new Set(marked);
    var available = new Set();
    bank.content.querySelectorAll('.exam-question').forEach(function (question) {
      var number = question.getAttribute('data-question');
      if (wanted.has(number)) { list.appendChild(question.cloneNode(true)); available.add(number); }
    });
    document.getElementById('mistake-empty').hidden = list.children.length > 0;
    var missing = marked.filter(function (n) { return !available.has(n); });
    var missingNode = document.getElementById('mistake-missing');
    missingNode.hidden = missing.length === 0;
    missingNode.textContent = '以下标记暂未收录在当前教材题目中：' + missing.join('、');
    var refresh = document.getElementById('mistake-retry');
    refresh.addEventListener('click', function () {
      // Carry current marks even on browsers that isolate storage for local files.
      location.href = location.pathname + location.search + '#marks=' + encodeURIComponent(JSON.stringify(marked));
      location.reload();
    });
  }
  sync();
})();
