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
  var isBook = document.body.hasAttribute('data-mistake-book');
  var isAway = isBook || document.body.hasAttribute('data-mock-exam');
  var returnPoint = null;
  var incomingReturn = null;
  function validPosition(value) {
    if (!value || typeof value.anchor !== 'string' || !/^[A-Za-z0-9_-]{1,100}$/.test(value.anchor) ||
        typeof value.offset !== 'number' || !Number.isFinite(value.offset) || Math.abs(value.offset) > 200000) return null;
    return {anchor:value.anchor, offset:value.offset};
  }
  function rememberReturn() {
    if (!isAway) return;
    try { sessionStorage.setItem(storageKey + '.return', JSON.stringify(returnPoint)); } catch (error) {}
  }
  if (isAway) {
    try { returnPoint = validPosition(JSON.parse(sessionStorage.getItem(storageKey + '.return'))); } catch (error) {}
  }
  marked = read();
  // Navigation snapshots work even when local files have separate browser storage.
  if (location.hash.indexOf('#marks=') === 0) {
    var params = new URLSearchParams(location.hash.slice(1));
    try {
      var incoming = JSON.parse(params.get('marks'));
      if (Array.isArray(incoming)) { marked = clean(incoming); save(); }
    } catch (error) { /* Keep saved marks if a link is malformed. */ }
    try { incomingReturn = validPosition(JSON.parse(params.get('return'))); } catch (error) {}
    if (incomingReturn) { returnPoint = incomingReturn; rememberReturn(); }
    try { history.replaceState(null, '', location.pathname + location.search); } catch (error) {}
  }
  function navigationHash() {
    return '#marks=' + encodeURIComponent(JSON.stringify(marked)) +
      (returnPoint ? '&return=' + encodeURIComponent(JSON.stringify(returnPoint)) : '');
  }
  function capturePosition() {
    if (isAway) return;
    var best = null;
    var bestTop = -Infinity;
    document.querySelectorAll('h2[id], h3[id], .exam-question').forEach(function (node) {
      if (!node.getClientRects().length) return;
      var top = node.getBoundingClientRect().top;
      if (top <= 80 && top >= bestTop) { best = node; bestTop = top; }
    });
    if (!best) best = document.querySelector('h2[id], h3[id]');
    if (best && best.classList.contains('exam-question')) best = best.querySelector('.quiz-image');
    if (best && best.id) returnPoint = validPosition({anchor:best.id, offset:best.getBoundingClientRect().top});
  }
  function restorePosition() {
    if (isAway || !incomingReturn) return;
    var target = document.getElementById(incomingReturn.anchor);
    if (!target) return;
    for (var parent = target.parentElement; parent; parent = parent.parentElement) {
      if (parent.tagName === 'DETAILS') parent.open = true;
    }
    var cancelled = false;
    var observer = null;
    function cancel() { cancelled = true; if (observer) observer.disconnect(); }
    ['wheel','touchstart','pointerdown','keydown'].forEach(function (type) {
      window.addEventListener(type, cancel, {once:true, passive:true});
    });
    function apply() {
      if (cancelled) return;
      var root = document.documentElement;
      var previous = root.style.scrollBehavior;
      root.style.scrollBehavior = 'auto';
      window.scrollTo(0, Math.max(0, target.getBoundingClientRect().top + window.scrollY - incomingReturn.offset));
      root.style.scrollBehavior = previous;
    }
    window.requestAnimationFrame(apply);
    function afterMath() {
      if (window.MathJax && window.MathJax.startup && window.MathJax.startup.promise) {
        window.MathJax.startup.promise.then(apply).catch(function () {});
      }
    }
    window.addEventListener('load', function () { apply(); afterMath(); }, {once:true});
    afterMath();
    if (window.ResizeObserver) {
      observer = new window.ResizeObserver(function () { window.requestAnimationFrame(apply); });
      observer.observe(document.querySelector('main') || document.body);
      window.setTimeout(function () { observer.disconnect(); }, 8000);
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', restorePosition, {once:true});
  else restorePosition();
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
      link.href = link.getAttribute('data-mistake-link') + navigationHash();
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
    if (link) { capturePosition(); sync(); }
  });
  ['pointerdown','contextmenu'].forEach(function (type) {
    document.addEventListener(type, function (event) {
      if (event.target.closest('[data-mistake-link]')) { capturePosition(); sync(); }
    });
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
      location.href = location.pathname + location.search + navigationHash();
      location.reload();
    });
  }
  sync();
})();
