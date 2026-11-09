(function (root) {
  'use strict';
  function shuffle(values, random) {
    var result = values.slice();
    for (var i = result.length - 1; i > 0; i--) {
      var j = Math.floor(random() * (i + 1));
      var temporary = result[i]; result[i] = result[j]; result[j] = temporary;
    }
    return result;
  }
  function draw(questions, themeIds, chapters, random) {
    random = random || Math.random;
    var pools = new Map();
    themeIds.forEach(function (theme) {
      var pool = questions.filter(function (q) { return q.theme === theme; });
      if (pool.length < 2) throw new Error('知识主题题量不足：' + theme);
      pools.set(theme, pool);
    });
    var slots = themeIds.flatMap(function (theme) { return [theme, theme]; });
    var candidates = new Map();
    chapters.forEach(function (chapter) {
      candidates.set(chapter, shuffle(slots.map(function (theme, index) { return index; }).filter(function (index) {
        return pools.get(slots[index]).some(function (q) { return q.chapter === chapter; });
      }), random));
    });
    // Match each chapter to one of the twenty theme slots, reassigning earlier slots when needed.
    var owners = new Map();
    function assign(chapter, visited) {
      return candidates.get(chapter).some(function (slot) {
        if (visited.has(slot)) return false;
        visited.add(slot);
        if (!owners.has(slot) || assign(owners.get(slot), visited)) {
          owners.set(slot, chapter); return true;
        }
        return false;
      });
    }
    shuffle(chapters, random).sort(function (a, b) { return candidates.get(a).length - candidates.get(b).length; }).forEach(function (chapter) {
      if (!assign(chapter, new Set())) throw new Error('无法同时覆盖知识主题与大章：' + chapter);
    });
    var selected = new Map();
    var used = new Set();
    var sections = new Set();
    var chapterCounts = new Map();
    function choose(slot, pool) {
      var options = pool.filter(function (q) { return !used.has(q.id); });
      var fresh = options.filter(function (q) { return !sections.has(q.section); });
      if (fresh.length) options = fresh;
      if (!options.length) throw new Error('题目不足，无法组成不重复的试卷');
      var smallest = Math.min.apply(null, options.map(function (q) { return chapterCounts.get(q.chapter) || 0; }));
      options = options.filter(function (q) { return (chapterCounts.get(q.chapter) || 0) === smallest; });
      var question = options[Math.floor(random() * options.length)];
      selected.set(slot, question); used.add(question.id); sections.add(question.section);
      chapterCounts.set(question.chapter, (chapterCounts.get(question.chapter) || 0) + 1);
    }
    owners.forEach(function (chapter, slot) {
      choose(slot, pools.get(slots[slot]).filter(function (q) { return q.chapter === chapter; }));
    });
    shuffle(slots.map(function (theme, index) { return index; }), random).forEach(function (slot) {
      if (!selected.has(slot)) choose(slot, pools.get(slots[slot]));
    });
    return shuffle(Array.from(selected.values()), random);
  }
  root.radioExamSampling = {draw:draw};
})(globalThis);
