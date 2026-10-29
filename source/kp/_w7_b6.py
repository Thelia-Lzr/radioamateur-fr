#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批次 7 第 6 盘：事实性小修正 + 渲染自检"""
import json, os, re, html

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out_7.json')
D = json.load(open(OUT, encoding='utf-8'))

# K105：运放例题的电阻值应与教材一致（–25k/5000 = –5）
D["K105"]["body"] = D["K105"]["body"].replace(
 "（15 kΩ 与 5 kΩ 例 → G = −5）", "（R2 = 25 kΩ、R1 = 5 kΩ → G = −5）"
)

# K098：法语的 7,200 MHz 就是 7,2 MHz，中文里写清楚，避免读成 7200 MHz
D["K098"]["body"] = D["K098"]["body"].replace(
 "（7,200 MHz 是 BLI 的载波频率）", "（BLI 的抑制载波为 7,2 MHz，法语写作 7,200 MHz）"
)

json.dump(D, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---------- 自检 ----------
def md2html(t):
    """复制 gen_deck_kp.py 的实现，用于确认渲染不炸"""
    t = (t or '').replace('\r', '')
    out, in_ul = [], False
    for raw in t.split('\n'):
        line = raw.rstrip()
        if not line.strip():
            if in_ul:
                out.append('</ul>'); in_ul = False
            continue
        body = html.escape(line.strip())
        body = body.replace('&quot;', '"').replace('&#x27;', "'")
        body = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', body)
        if body.startswith('## '):
            if in_ul:
                out.append('</ul>'); in_ul = False
            out.append('<div class="h4">%s</div>' % body[3:])
        elif re.match(r'^[-·]\s+', body):
            if not in_ul:
                out.append('<ul class="ul">'); in_ul = True
            out.append('<li>%s</li>' % re.sub(r'^[-·]\s+', '', body))
        else:
            if in_ul:
                out.append('</ul>'); in_ul = False
            out.append('<p class="p">%s</p>' % body)
    if in_ul:
        out.append('</ul>')
    return ''.join(out)

bad = 0
for k in sorted(D):
    v = D[k]
    h = md2html(v['body'])
    f = md2html(v['front'])
    # 未闭合的 ** 或多余的 < >
    if v['body'].count('**') % 2:
        print('!! 粗体未配对', k); bad += 1
    if '|' in v['body']:
        print('!! 含竖线（表格不会被渲染）', k); bad += 1
    if '\\(' in v['body'] and '\\)' not in v['body'].replace('\\(', '', 1):
        pass
    opens = len(re.findall(r'\\\(', v['body'])) + len(re.findall(r'\\\[', v['body']))
    closes = len(re.findall(r'\\\)', v['body'])) + len(re.findall(r'\\\]', v['body']))
    if opens != closes:
        print('!! 数学定界符不配对', k, opens, closes); bad += 1
    if '<' in h and not re.search(r'<(b|/b|ul|/ul|li|/li|p|/p|div|/div)\b', h):
        print('!! 意外标签', k); bad += 1
    n = sum(1 for c in v['body'] if '\u4e00' <= c <= '\u9fff')
    print(k, '汉字', n, '| html组块', len(h))
print('问题数:', bad)
print('待核:', [(k, v['body'].count('⚠️待核')) for k, v in D.items() if '⚠️待核' in v['body']])
