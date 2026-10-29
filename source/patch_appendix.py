#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用核对结果重建教材附录 G（待核实事项汇总）。

用法：python3 patch_appendix.py --apply
"""
import json, re, os, sys, html, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
MANUEL = os.path.join(os.path.dirname(BASE), 'manuel-zh.html')
APPLY = '--apply' in sys.argv

pend = json.load(open(os.path.join(BASE, 'manual_pending.json'), encoding='utf-8'))
res = json.load(open(os.path.join(BASE, 'manual_fix', 'merged.json'), encoding='utf-8'))
s = open(MANUEL, encoding='utf-8').read()

TAG = re.compile(r'<[^>]+>')
def strip_tags(x):
    return re.sub(r'\s+', ' ', html.unescape(TAG.sub('', x))).strip()

KEYOVR = {'P42': '没有解释工程上为什么普遍选',
          'P24': '用什么仪表测量非常大的电流'}

def key_of(it):
    pid = it['id']
    k = re.sub(r'^⚠️?\s*待核实?\s*[：:]?\s*', '', it['text']).strip()[:36]
    k = KEYOVR.get(pid) or k
    return k.replace('"', '').replace('\u201c', '').replace('\u201d', '')

keys = [(key_of(it), it['id']) for it in pend if key_of(it)]

# 定位附录 G 的 <ol>…</ol>
start = s.index('<h3 id="annexe-g">')      # 附录 G 是最后一节
end = s.find('</main>', start)
if end < 0:
    end = len(s)
block = s[start:end]
class _M:  # 保持后面的 m.start()/m.end() 接口
    def __init__(self, a, b): self._a, self._b = a, b
    def start(self): return self._a
    def end(self): return self._b
m = _M(start, end)
om = re.search(r'<ol>.*?</ol>', block, re.S)
assert om, '附录里没有 <ol>'

items = re.findall(r'<li>(.*?)</li>', om.group(0), re.S)
print('附录列表项:', len(items))

LABEL = {'resolved': ('✅', '已核实'),
         'source_defect': ('⚠️', '题库／原文有误'),
         'not_in_source': ('📌', '本节未涉及')}

out, unmatched, counts = [], 0, {}
for li in items:
    plain = strip_tags(li)
    sec = ''
    sm = re.search(r'<b>(§[^<]*)</b>', li)
    if sm:
        sec = sm.group(1)
    hit = None
    for k, pid in keys:
        if k and k in plain:
            hit = pid
            break
    if hit is None:                       # 退一步用短键
        for k, pid in keys:
            if k[:18] and k[:18] in plain:
                hit = pid
                break
    if hit is None or hit not in res:
        unmatched += 1
        out.append('<li><b>%s</b>：%s</li>' % (sec, plain))
        continue
    r = res[hit]
    v = r.get('verdict', '')
    counts[v] = counts.get(v, 0) + 1
    icon, label = LABEL.get(v, ('•', ''))
    ans = html.escape(str(r.get('answer', ''))).replace('&lt;br&gt;', '<br>')
    src = str(r.get('source', '') or '')
    out.append('<li><b>%s</b>：%s <b>%s</b> %s%s</li>' % (
        sec, icon, label, ans,
        ('<span class="src">（来源：%s）</span>' % html.escape(src)) if src else ''))

new_ol = '<ol>' + ''.join(out) + '</ol>'
new_intro = ('<p>下面这些地方，F6KGL 教材原文没有写清楚、或者不同资料之间有出入。'
             '本教材在 <b>2026-10-07</b> 逐条核对了一遍——原始 PDF 全文（含表格与插图）、'
             '题库官方注释、原书习题解答、以及 ANFR／ARCEP／CEPT 官方文件。'
             '每条的结论与来源都写在下面；仍未查实的，如实标注。</p>')

print('未能匹配:', unmatched)
print('verdict 统计:', counts)

if APPLY:
    shutil.copyfile(MANUEL, MANUEL + '.bak-before-appendix')
    nb = re.sub(r'<ol>.*?</ol>', lambda _: new_ol, block, flags=re.S)
    nb = re.sub(r'<p>下面这些地方.*?</p>', lambda _: new_intro, nb, count=1, flags=re.S)
    nb = nb.replace('生成时间：2026-10-01', '待核核对：2026-10-07')
    s = s[:m.start()] + nb + s[m.end():]
    open(MANUEL, 'w', encoding='utf-8').write(s)
    print()
    print('已写回。剩余「待核」:', s.count('待核'))
    print('备份:', MANUEL + '.bak-before-appendix')
