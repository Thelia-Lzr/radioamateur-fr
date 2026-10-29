#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分块工具：给撰写者输出「本批题目 + 对应教材章节摘录」。

用法：
  python3 ground.py part 0              # 第 0 块（默认把 227 题分成 NPART 块）
  python3 ground.py part 0 --budget 2500
  python3 ground.py anchor T112a        # 单独看某个锚点的整节教材文字
  python3 ground.py num 20617           # 单独看某题的锚点整节文字
数据源：slice_2.json + 项目根目录的 manuel-zh.html（中文教材，带锚点）
"""
import re
import sys
import html
import json
import os

BASE = '/home/thelia/Documents/radioamateur-fr'
SLICE = os.path.join(BASE, 'source/explain/slice_2.json')
MANUEL = os.path.join(BASE, 'manuel-zh.html')
NPART = 5


def to_text(frag):
    frag = re.sub(r'(?i)</(p|li|tr|div|h3|h2|td|th)>', '\n', frag)
    frag = re.sub(r'(?i)<br\s*/?>', '\n', frag)
    frag = re.sub(r'(?i)</t[dh]>', ' | ', frag)
    frag = re.sub(r'<[^>]+>', '', frag)
    frag = html.unescape(frag)
    lines = [re.sub(r'[ \t\u00a0]+', ' ', l).strip() for l in frag.split('\n')]
    return '\n'.join(l for l in lines if l)


def load_sections():
    h = open(MANUEL, encoding='utf-8').read()
    chunks = re.split(r'(?=<h[23][ >])', h)
    secs = {}
    for c in chunks:
        m = re.match(r'<h[23][^>]*id="([^"]+)"', c)
        if not m:
            continue
        ids = [m.group(1)] + re.findall(r'<span class="anch" id="([^"]+)"', c)
        txt = to_text(c)
        for i in ids:
            secs.setdefault(i, txt)
    return secs


SECTIONS = load_sections()


def bigrams(s):
    s = re.sub(r'[^\u4e00-\u9fffA-Za-z0-9µΩ.,]+', '', s)
    cjk = re.findall(r'[\u4e00-\u9fff]', s)
    bg = set(''.join(cjk[i:i + 2]) for i in range(len(cjk) - 1))
    bg |= set(w.lower() for w in re.findall(r'[A-Za-z0-9µΩ]{2,}', s))
    return bg


def excerpt(anchor, items, budget=2000):
    txt = SECTIONS.get(anchor)
    if not txt:
        return None
    if len(txt) <= budget:
        return txt
    kws = set()
    ans = set()
    for q in items:
        blob = ' '.join([q.get('stem_zh', ''), q.get('ans_zh', ''), q.get('com_zh', ''),
                         q.get('theme_zh', '')])
        kws |= bigrams(blob)
        ans |= bigrams(q.get('ans_zh', '')) | bigrams(q.get('ans_fr', ''))
    lines = txt.split('\n')
    scored = []
    for i, l in enumerate(lines):
        b = bigrams(l)
        sc = len(b & kws) + 3 * len(b & ans)
        # 表格行、含数字的行给一点基础分
        if re.search(r'\d', l):
            sc += 0.5
        scored.append((sc, i))
    keep = set(range(min(3, len(lines))))  # 开头几行（标题/总述）
    used = sum(len(lines[i]) for i in keep)
    for sc, i in sorted(scored, key=lambda t: -t[0]):
        if len(keep) >= 3 + 14:
            break
        if used + len(lines[i]) > budget:
            continue
        if i in keep:
            continue
        keep.add(i)
        used += len(lines[i])
    out = '\n'.join(lines[i] for i in sorted(keep))
    return out


def parts():
    d = json.load(open(SLICE, encoding='utf-8'))
    n = len(d)
    size = (n + NPART - 1) // NPART
    return [d[i:i + size] for i in range(0, n, size)]


def show_part(k, budget=2000):
    d = parts()[k]
    print(f'=== PART {k} : {len(d)} 题  {d[0]["num"]} … {d[-1]["num"]} ===\n')
    groups = {}
    for q in d:
        groups.setdefault(q['anchor'], []).append(q)
    for anchor, items in groups.items():
        print(f'---------- 教材锚点 {anchor} （{len(items)} 题） ----------')
        ex = excerpt(anchor, items, budget)
        if ex is None:
            print('!! 教材中没有这个锚点：请依据法语原题与注释推理，'
                  '拿不准时写「按教材对应章节核对」或「⚠️待核」\n')
        else:
            print(ex, '\n')
        for q in items:
            print(f'--- 题号 {q["num"]} | 主题 {q["theme_zh"]} / {q["theme_fr"]}')
            print(f'法文题干: {q["stem_fr"]}')
            print(f'中文题干: {q["stem_zh"]}')
            for j, o in enumerate(q['options']):
                mark = ' <=正确答案' if j == q['ans_idx'] else ''
                print(f'   [{j}] {o}{mark}')
            print(f'答案: {q["ans_fr"]} / {q["ans_zh"]}')
            if q.get('commentaire_fr', '').strip():
                print(f'官方注释(法): {q["commentaire_fr"].strip()}')
            if q.get('com_zh', '').strip():
                print(f'官方注释(中): {q["com_zh"].strip()}')
            print()


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return
    mode, val = sys.argv[1], sys.argv[2]
    budget = 2000
    if '--budget' in sys.argv:
        budget = int(sys.argv[sys.argv.index('--budget') + 1])
    if mode == 'part':
        show_part(int(val), budget)
    elif mode == 'anchor':
        print(SECTIONS.get(val, '（没有这个锚点）'))
    elif mode == 'num':
        d = json.load(open(SLICE, encoding='utf-8'))
        q = next(x for x in d if x['num'] == val)
        print(f'锚点 {q["anchor"]}\n')
        print(SECTIONS.get(q['anchor'], '（没有这个锚点）'))
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
