#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 47 条待核的核对结果写回教材 manuel-zh.html。

用法：
  python3 patch_manual.py          # 干跑，只报告匹配情况
  python3 patch_manual.py --apply  # 实际改写（会先备份）
"""
import json, re, os, sys, html, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
MANUEL = os.path.join(os.path.dirname(BASE), 'manuel-zh.html')
PEND = os.path.join(BASE, 'manual_pending.json')
MERGED = os.path.join(BASE, 'manual_fix', 'merged.json')

APPLY = '--apply' in sys.argv

pend = json.load(open(PEND, encoding='utf-8'))
res = json.load(open(MERGED, encoding='utf-8'))
s = open(MANUEL, encoding='utf-8').read()
orig_len = len(s)


def md_table_to_html(md):
    """把 Markdown 表格转成 HTML 表格；非表格返回 None"""
    lines = [l.strip() for l in md.strip().split('\n') if l.strip()]
    rows = [l for l in lines if l.startswith('|')]
    if len(rows) < 2:
        return None
    def cells(l):
        return [c.strip() for c in l.strip('|').split('|')]
    out = ['<table class="mdtab">']
    for i, r in enumerate(rows):
        cs = cells(r)
        if i == 1 and all(re.fullmatch(r':?-{2,}:?', c or '-') for c in cs):
            continue                      # 分隔行
        tag = 'th' if i == 0 else 'td'
        out.append('<tr>' + ''.join('<%s>%s</%s>' % (tag, c, tag) for c in cs) + '</tr>')
    out.append('</table>')
    return ''.join(out)


def body_to_html(txt):
    """把答案正文转成 HTML：Markdown 表格转 <table>，其余分段"""
    txt = (txt or '').strip()
    if not txt:
        return ''
    parts, buf, in_tab = [], [], []
    for line in txt.split('\n'):
        if line.strip().startswith('|'):
            in_tab.append(line)
            continue
        if in_tab:
            t = md_table_to_html('\n'.join(in_tab))
            if t:
                parts.append(t)
            else:
                buf.extend(in_tab)
            in_tab = []
        if line.strip():
            buf.append(line.strip())
        else:
            if buf:
                parts.append('<p>' + html.escape(' '.join(buf)).replace('&lt;', '<').replace('&gt;', '>') + '</p>')
                buf = []
    if in_tab:
        t = md_table_to_html('\n'.join(in_tab))
        parts.append(t if t else html.escape(' '.join(in_tab)))
    if buf:
        parts.append('<p>' + html.escape(' '.join(buf)).replace('&lt;', '<').replace('&gt;', '>') + '</p>')
    return ''.join(parts)


def style_for(verdict):
    if verdict == 'source_defect':
        return 'warn', '⚠️ 题库／原文有误'
    if verdict == 'not_in_source':
        return 'note', '📌 本节未涉及'
    return 'note', '✅ 已核实'


# 抽取所有警示/说明块（这些块内部无嵌套 div），逐块去标签后与待核句比对
BLOCK = re.compile(r'<div class="(warn|note|tips|formula)"[^>]*>.*?</div>', re.S)
TAG = re.compile(r'<[^>]+>')

def strip_tags(x):
    return re.sub(r'\s+', ' ', html.unescape(TAG.sub('', x))).strip()

blocks = [(m.start(), m.end(), m.group(0), strip_tags(m.group(0)))
          for m in BLOCK.finditer(s)]
blocks_with_pending = [b for b in blocks if '待核' in b[3]]
print('警示块总数:', len(blocks), '| 含待核的块:', len(blocks_with_pending))
print()

REPLACEMENTS = []
matched, misses = 0, []
used = set()
for it in pend:
    pid = it['id']
    r = res.get(pid)
    if not r:
        misses.append((pid, it['text'][:60], '无核对结果'))
        continue
    # 用待核句的前 36 个字符（去掉标记）作定位键
    KEYOVR = {'P42': '没有解释工程上为什么普遍选',
              'P24': '用什么仪表测量非常大的电流',
              'P01': None}   # P01 是目录行，不是警示块，另行处理
    key = re.sub(r'^⚠️?\s*待核实?\s*[：:]?\s*', '', it['text']).strip()[:36]
    if pid in KEYOVR and KEYOVR[pid] is None:
        misses.append((pid, it['text'][:60], '目录行，需单独处理'))
        continue
    key = KEYOVR.get(pid) or key
    key = key.replace('"', '').replace('\u201c', '').replace('\u201d', '')
    if not key:
        misses.append((pid, it['text'][:60], '键为空'))
        continue
    # 在已抽取的块里找包含该键的那一块
    hit = None
    for i, b in enumerate(blocks_with_pending):
        if i in used:
            continue
        if key and key in b[3]:
            hit, idx = b, i
            break
    if hit is None:
        # 退一步：缩到 20 字再试
        short = key[:20]
        for i, b in enumerate(blocks_with_pending):
            if i in used:
                continue
            if short and short in b[3]:
                hit, idx = b, i
                break
    if hit is None:
        misses.append((pid, key, '未在警示块中定位到'))
        continue
    used.add(idx)
    matched += 1
    cls, label = style_for(r.get('verdict', ''))
    inner = body_to_html(r.get('answer', ''))
    src = r.get('source', '')
    note = r.get('note', '')
    foot = []
    if src:
        foot.append('来源：' + html.escape(str(src)))
    if note:
        foot.append(html.escape(str(note)))
    block = '<div class="%s"><b>%s</b>%s%s</div>' % (
        cls, label, inner,
        ('<p class="src">' + ' ｜ '.join(foot) + '</p>') if foot else '')
    REPLACEMENTS.append((hit[0], hit[1], block))

print('待核条目:', len(pend), '| 已定位:', matched, '| 未定位:', len(misses))
for pid, k, why in misses:
    print(f'   ✗ {pid}  {k[:52]}  ——  {why}')

if APPLY:
    # 关键：偏移量都是基于原始字符串，必须从后往前替换，否则会互相错位
    for a, b, blk in sorted(REPLACEMENTS, key=lambda x: -x[0]):
        s = s[:a] + blk + s[b:]
    shutil.copyfile(MANUEL, MANUEL + '.bak-before-verify')
    open(MANUEL, 'w', encoding='utf-8').write(s)
    print()
    print('已写回，长度', orig_len, '→', len(s))
    print('剩余「待核」:', s.count('待核'))
    print('备份:', MANUEL + '.bak-before-verify')
