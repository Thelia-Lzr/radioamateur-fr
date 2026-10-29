#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""自检一个 part 文件：python3 check_part.py <part 号>
检查：格式可解析、题号与本批（slice_2.json）完全一致、条数、长度、禁用符号。
"""
import os
import re
import sys
import json

BASE = '/home/thelia/Documents/radioamateur-fr/source/explain'
NPART = 5


def parse(path):
    txt = open(path, encoding='utf-8').read().replace('\r\n', '\n')
    out, cur, buf = {}, None, []
    for line in txt.split('\n'):
        m = re.match(r'###\s*(\d{4,6})\s*$', line.strip())
        if m:
            if cur is not None:
                out[cur] = '\n'.join(buf).strip()
            cur, buf = m.group(1), []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = '\n'.join(buf).strip()
    return out


def main():
    k = int(sys.argv[1])
    d = json.load(open(os.path.join(BASE, 'slice_2.json'), encoding='utf-8'))
    size = (len(d) + NPART - 1) // NPART
    want = [q['num'] for q in d[k * size:(k + 1) * size]]
    path = os.path.join(BASE, 'parts', f'part_{k}.txt')
    if not os.path.exists(path):
        print(f'!! 还没有 {path}')
        return 1
    got = parse(path)
    missing = [n for n in want if n not in got]
    extra = [n for n in got if n not in want]
    bad = []
    for n, t in got.items():
        plain = re.sub(r'\\\(.*?\\\)|\\\[.*?\\\]', '', t, flags=re.S)
        allch = len(re.sub(r'\s', '', plain))
        if allch < 80:
            bad.append((n, 'too_short', allch))
        elif allch > 300:
            bad.append((n, 'too_long', allch))
        if '$' in t:
            bad.append((n, 'dollar_math', 0))
        if not re.search(r'[\u4e00-\u9fff]', t):
            bad.append((n, 'no_chinese', 0))
    print(f'part {k}: 应有 {len(want)} 条，实有 {len(got)} 条')
    if missing:
        print(f'!! 缺 {len(missing)}: {missing}')
    if extra:
        print(f'!! 多 {len(extra)}: {extra}')
    if bad:
        print(f'!! 不合格 {len(bad)}:')
        for b in bad:
            print('   ', b)
    if not (missing or extra or bad):
        print('OK ✓ 全部合规')
    todos = [n for n, t in got.items() if '待核' in t]
    if todos:
        print(f'标了待核 {len(todos)} 条: {todos}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
