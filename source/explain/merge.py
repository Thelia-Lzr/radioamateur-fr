#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""合并 parts/*.txt 为 out_2.json，并校验。

parts 文件格式（UTF-8，纯文本）：

### 20573
讲解正文，可以多行，可以含 \( ... \) 与 \[ ... \]

### 20578
……

行首为 "### 数字" 的行开一条新记录；正文里禁止出现行首的 "### "。
"""
import os
import re
import sys
import json
import glob

BASE = '/home/thelia/Documents/radioamateur-fr/source/explain'
SLICE = os.path.join(BASE, 'slice_2.json')
OUT = os.path.join(BASE, 'out_2.json')


def parse(path):
    txt = open(path, encoding='utf-8').read().replace('\r\n', '\n')
    out = {}
    cur = None
    buf = []
    for line in txt.split('\n'):
        m = re.match(r'###\s*(\d{4,6})\s*$', line.strip())
        if m:
            if cur is not None:
                out[cur] = '\n'.join(buf).strip()
            cur = m.group(1)
            buf = []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = '\n'.join(buf).strip()
    return out


def main():
    d = json.load(open(SLICE, encoding='utf-8'))
    want = [q['num'] for q in d]
    data = {}
    for p in sorted(glob.glob(os.path.join(BASE, 'parts', '*.txt'))):
        part = parse(p)
        dup = set(part) & set(data)
        if dup:
            print(f'!! {p}: 重复题号 {sorted(dup)}')
        data.update(part)
    unknown = [k for k in data if k not in set(want)]
    if unknown:
        print(f'!! 不属于本批的题号（已忽略）: {unknown}')
        for k in unknown:
            data.pop(k)
    missing = [n for n in want if n not in data]
    # 逐条体检
    problems = []
    for n, t in data.items():
        body = re.sub(r'\\\(.*?\\\)|\\\[.*?\\\]', '', t, flags=re.S)
        cn = len(re.findall(r'[\u4e00-\u9fff]', body))
        allch = len(re.sub(r'\s', '', body))
        if allch < 80:
            problems.append((n, 'too_short', allch, t[:60]))
        elif allch > 300:
            problems.append((n, 'too_long', allch, t[:60]))
        if '$' in t:
            problems.append((n, 'dollar', 0, t[:60]))
        lat = len(re.findall(r'[A-Za-z]', body))
        if lat > allch * 0.5:
            problems.append((n, 'too_much_latin', lat, t[:60]))
        if '待核' in t:
            problems.append((n, 'TODO_CHECK', 0, t[:80]))
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    json.load(open(OUT, encoding='utf-8'))
    print(f'写入 {OUT}: {len(data)} 条（应含 {len(want)} 条）')
    if missing:
        print(f'!! 缺失 {len(missing)} 条: {missing}')
    print(f'!  体检问题 {len(problems)} 条:')
    for p in problems:
        print('   ', p)
    return 0 if not missing else 1


if __name__ == '__main__':
    sys.exit(main())
