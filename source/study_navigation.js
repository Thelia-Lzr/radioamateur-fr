(function () {
  'use strict';
  var sidebar = document.getElementById('study-sidebar');
  if (!sidebar) return;
  var toggle = document.querySelector('[data-sidebar-toggle]');
  var mobile = window.matchMedia('(max-width:900px)');
  function setOpen(open, focus) {
    document.body.setAttribute('data-sidebar-open', String(open));
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? '收起目录侧边栏' : '展开目录侧边栏');
    sidebar.inert = !open;
    if (focus) toggle.focus({preventScroll:true});
  }
  setOpen(!mobile.matches);
  toggle.addEventListener('click', function () { setOpen(toggle.getAttribute('aria-expanded') !== 'true'); });
  document.querySelector('[data-sidebar-close]').addEventListener('click', function () { setOpen(false, true); });
  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true' &&
        (mobile.matches || sidebar.contains(event.target))) { setOpen(false, true); event.preventDefault(); }
  });
  if (mobile.addEventListener) mobile.addEventListener('change', function () { setOpen(!mobile.matches); });

  var main = document.querySelector('main');
  var links = Array.from(sidebar.querySelectorAll('a[href^="#"]'));
  var navigationIds = new Set(links.map(function (link) { var target = targetFor(link.hash); return target && target.id; }));
  var headings = Array.from(main.querySelectorAll('[id]')).filter(function (node) { return navigationIds.has(node.id); });
  var current = null;
  var scheduled = false;
  var stopCorrection = function () {};
  function targetFor(hash) {
    try { return document.getElementById(decodeURIComponent(hash.slice(1))); }
    catch (error) { return null; }
  }
  function highlight(id) {
    if (current === id) return;
    current = id;
    links.forEach(function (link) {
      if (targetFor(link.hash) && targetFor(link.hash).id === id) {
        link.setAttribute('aria-current', 'location');
        var chapter = link.closest('.toc-chapter');
        if (chapter) chapter.open = true;
      } else link.removeAttribute('aria-current');
    });
  }
  function updateCurrent() {
    scheduled = false;
    var active = null;
    headings.forEach(function (heading) {
      if (heading.getClientRects().length && heading.getBoundingClientRect().top <= 56) active = heading;
    });
    highlight(active ? active.id : null);
  }
  function scheduleCurrent() {
    if (!scheduled) { scheduled = true; window.requestAnimationFrame(updateCurrent); }
  }
  function jump(hash, focus) {
    var target = targetFor(hash);
    if (!target || !main.contains(target)) return false;
    stopCorrection();
    for (var parent = target.parentElement; parent; parent = parent.parentElement) {
      if (parent.tagName === 'DETAILS') parent.open = true;
    }
    var cancelled = false;
    var observer = null;
    var frame = null;
    function apply() {
      frame = null;
      if (cancelled) return;
      // A direct jump avoids smooth scrolling across thousands of exercise cards.
      var root = document.documentElement;
      var previous = root.style.scrollBehavior;
      root.style.scrollBehavior = 'auto';
      window.scrollTo(0, Math.max(0, target.getBoundingClientRect().top + window.scrollY - 24));
      root.style.scrollBehavior = previous;
      scheduleCurrent();
    }
    function schedule() { if (!cancelled && frame === null) frame = window.requestAnimationFrame(apply); }
    function stop() {
      cancelled = true;
      if (observer) observer.disconnect();
      if (frame !== null) window.cancelAnimationFrame(frame);
      ['wheel', 'touchstart', 'pointerdown', 'keydown'].forEach(function (type) { window.removeEventListener(type, stop); });
      main.removeEventListener('load', schedule, true);
      window.removeEventListener('load', schedule);
      window.clearTimeout(timeout);
    }
    stopCorrection = stop;
    ['wheel', 'touchstart', 'pointerdown', 'keydown'].forEach(function (type) { window.addEventListener(type, stop, {passive:true}); });
    main.addEventListener('load', schedule, true);
    window.addEventListener('load', schedule);
    if (window.ResizeObserver) {
      observer = new window.ResizeObserver(schedule);
      observer.observe(main);
    }
    var timeout = window.setTimeout(function () {
      if (observer) observer.disconnect();
      main.removeEventListener('load', schedule, true);
    }, 10000);
    if (document.fonts) document.fonts.ready.then(schedule);
    if (window.MathJax && window.MathJax.startup && window.MathJax.startup.promise) {
      window.MathJax.startup.promise.then(schedule).catch(function () {});
    }
    if (focus) {
      if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
      target.focus({preventScroll:true});
    }
    highlight(target.id);
    apply();
    schedule();
    return true;
  }
  document.addEventListener('click', function (event) {
    if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    var link = event.target.closest('a[href^="#"]');
    if (!link || link.hasAttribute('download') || (link.target && link.target !== '_self')) return;
    var target = targetFor(link.hash);
    if (!target || !main.contains(target)) return;
    event.preventDefault();
    if (mobile.matches && sidebar.contains(link)) setOpen(false);
    if (location.hash !== link.hash) history.pushState(history.state, '', link.hash);
    jump(link.hash, true);
  });
  window.addEventListener('hashchange', function () { jump(location.hash, false); });
  window.addEventListener('scroll', scheduleCurrent, {passive:true});
  window.addEventListener('resize', scheduleCurrent);
  if (location.hash) jump(location.hash, false);
  scheduleCurrent();
})();
