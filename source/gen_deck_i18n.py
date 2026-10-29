#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""在「含真题例句」卡组基础上，为每条例句加上中文翻译，生成新的 .apkg。
依赖：translations_1.json / translations_2.json / translations_3.json
用法：<venv>/bin/python gen_deck_i18n.py
"""
import csv, json, os, re, html, glob, unicodedata
import genanki

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_CSV = os.path.join(BASE, 'data', 'vocabulaire.csv')
SRC_Q = os.path.join(BASE, 'source', 'Exam1', 'questions', 'questions.json')
OUT = os.path.join(BASE, 'decks', '无线电词汇（中译例句＋原题图）.apkg')
IMGDIR = os.path.join(BASE, 'source', 'Exam1', 'questions')

MAX_EX = 2
MAX_QLEN = 260

# ---------- 工具 ----------
def strip_acc(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn').lower()

def toks(s):
    return set(re.findall(r"[a-z0-9]+", strip_acc(s)))

def flat(s):
    """归一化：去重音、转小写、折叠所有空白"""
    return re.sub(r'\s+', ' ', strip_acc(s)).strip()

ACC = {'a': '[aàâä]', 'e': '[eéèêë]', 'i': '[iîï]', 'o': '[oôö]',
       'u': '[uùûü]', 'c': '[cç]', 'y': '[yÿ]'}

def word_regex(w):
    out = []
    for ch in w:
        low = strip_acc(ch)
        out.append(ACC[low] if (low.isalpha() and low in ACC) else re.escape(ch))
    return re.compile(''.join(out), re.IGNORECASE)

def mark(text, word):
    """目标词加粗；先转义 HTML，再把标记还原"""
    esc = html.escape(text)
    pat = word_regex(html.escape(word))
    esc = pat.sub(lambda m: '<b>' + m.group(0) + '</b>', esc, count=2)
    return esc

# 法语「点号作千位分隔」：数字.恰好三位数字
THOU = re.compile(r'\d\.\d{3}(?!\d)')

# ---------- 载入 ----------
rows = list(csv.DictReader(open(SRC_CSV, encoding='utf-8')))
qs = json.load(open(SRC_Q, encoding='utf-8'))['questions']

# 合并三批译文
TR = {}
for f in sorted(glob.glob(os.path.join(BASE, 'source', 'translations_*.json'))):
    part = json.load(open(f, encoding='utf-8'))
    TR.update(part)
    print('载入译文', os.path.basename(f), len(part), '条')
print('译文合计', len(TR), '条')

stem_t = [toks(q['question']) for q in qs]
all_t = [toks(q['question'] + ' ' + ' '.join(q['propositions'])) for q in qs]
stem_s = [flat(q['question']) for q in qs]
all_s = [flat(q['question'] + ' ' + ' '.join(q['propositions'])) for q in qs]

def pick(word, limit=MAX_EX):
    wn = strip_acc(word)
    single = len(re.findall(r"[a-z0-9]+", wn)) == 1
    sc = []
    for i, q in enumerate(qs):
        if single:
            if wn not in all_t[i]:
                continue
            ins = wn in stem_t[i]
        else:
            if wn not in all_s[i]:
                continue
            ins = wn in stem_s[i]
        L = len(all_s[i])
        if L > MAX_QLEN:
            continue
        sc.append(((3 if ins else 0) + (1 if q.get('commentaire') else 0) - L / 400.0, i))
    sc.sort(reverse=True)
    # 去重：题干 + 答案完全相同视为同一题（题库里有重复条目、编号不同）
    out, seen = [], set()
    for _, i in sc:
        rep = qs[i]['reponse']
        ans = qs[i]['propositions'][rep] if isinstance(rep, int) and 0 <= rep < len(qs[i]['propositions']) else ''
        key = (stem_s[i], flat(ans))
        if key in seen:
            continue
        seen.add(key)
        out.append(i)
        if len(out) >= limit:
            break
    return out

def zh(num, key):
    v = TR.get(str(num))
    return (v or {}).get(key, '') if isinstance(v, dict) else ''

MEDIA = set()          # 收集用到的图片

def img_for(num):
    """返回该题的原题图文件名（若存在）"""
    fn = '%s.png' % num
    p = os.path.join(IMGDIR, fn)
    if os.path.exists(p):
        MEDIA.add(p)
        return fn
    return ''

def render(examples, word):
    if not examples:
        return ''
    p = ['<div class="exwrap"><div class="extitle">真题例句</div>']
    for qi in examples:
        q = qs[qi] if isinstance(qi, int) else qi
        num = str(q['num'])
        raw = q['question']
        rep = q['reponse']
        ans = q['propositions'][rep] if isinstance(rep, int) and 0 <= rep < len(q['propositions']) else ''
        com = str(q.get('commentaire') or '')

        p.append('<div class="ex">')
        img = img_for(num)
        if img:
            p.append('<details class="eximg"><summary>查看原题图</summary>'
                     '<img src="%s"></details>' % img)
        p.append('<div class="exq">%s</div>' % mark(raw, word))
        t = zh(num, 'stem')
        if t:
            p.append('<div class="exzh">%s</div>' % html.escape(t))
        if ans:
            p.append('<div class="exa">&#10003; %s</div>' % html.escape(ans))
        ta = zh(num, 'answer')
        if ta and ta.strip() != ans.strip():
            p.append('<div class="exzh">%s</div>' % html.escape(ta))
        if com:
            p.append('<div class="exc">%s</div>' % html.escape(com))
            tc = zh(num, 'com')
            if tc:
                p.append('<div class="exzh">%s</div>' % html.escape(tc))
        # 千位分隔歧义提示（仅相关条目）
        if THOU.search(raw) or THOU.search(ans) or THOU.search(com):
            p.append('<div class="exw">注意：法语原文里点号常作千位分隔，'
                     '如 14.000 表示 14000</div>')
        p.append('</div>')
    p.append('</div>')
    return ''.join(p)

# ---------- 卡片样式与模板 ----------
CSS = """
.card { font-family:"Noto Sans CJK SC","Source Han Sans SC",sans-serif;
  font-size:22px; text-align:center; color:#1c1c1c; background:#fdfdfb; padding:18px 14px; }
.fr { font-size:34px; font-weight:600; margin-bottom:6px; }
.hint { color:#777; font-size:15px; }
.zh { font-size:30px; font-weight:600; margin:10px 0 14px; color:#14508c; }
.meta { margin:0 auto; border-collapse:collapse; font-size:15px; color:#444; }
.meta td { border-top:1px solid #ddd; padding:4px 10px; text-align:left; }
.meta td.k { color:#888; white-space:nowrap; }
.note { font-size:15px; color:#555; margin-top:12px; max-width:34em; line-height:1.5; margin-left:auto;margin-right:auto; }
hr#answer { border:none; border-top:1px solid #ddd; margin:14px auto; width:60%; }
.exwrap { margin:16px auto 0; max-width:36em; text-align:left; }
.extitle { font-size:18px; font-weight:600; color:#333; border-bottom:2px solid #14508c; padding-bottom:4px; margin-bottom:8px; }
.ex { background:#f4f6f2; border-left:3px solid #14508c; padding:8px 12px; margin-bottom:10px; border-radius:0 6px 6px 0; }
.exq { font-size:17px; line-height:1.45; color:#222; }
.exq b { color:#b3261e; }
.exzh { font-size:15px; color:#4a6b8a; line-height:1.5; margin-top:2px; }
.exa { font-size:16px; color:#1a6b34; margin-top:6px; font-weight:600; }
.exc { font-size:14px; color:#5a5a5a; margin-top:6px; font-style:italic; line-height:1.45;
  border-top:1px dashed #ccc; padding-top:5px; }
.exw { font-size:13px; color:#a15c00; margin-top:5px; }
.eximg { margin:0 0 7px 0; }
.eximg summary { cursor:pointer; font-size:14px; color:#14508c; font-weight:600;
  display:inline-block; padding:2px 8px; border:1px solid #cdd8e4; border-radius:4px;
  background:#eef3f8; list-style:none; }
.eximg summary::-webkit-details-marker { display:none; }
.eximg[open] summary { margin-bottom:6px; }
.eximg img { display:block; max-width:100%; height:auto; border:1px solid #d5d5d0;
  border-radius:5px; background:#fff; }
"""

QFMT = '<div class="fr">{{Français}}</div><div class="hint">{{类别}}</div>'
AFMT = """<div class="fr">{{Français}}</div>
<hr id="answer">
<div class="zh">{{中文}}</div>
<table class="meta">
<tr><td class="k">类别</td><td>{{类别}}</td></tr>
<tr><td class="k">主题</td><td>{{主题}}</td></tr>
<tr><td class="k">考题频次</td><td>{{频次}}</td></tr>
</table>
{{#备注}}<div class="note">{{备注}}</div>{{/备注}}
{{例句}}"""

FIELDS = ['Français', '中文', '类别', '主题', '频次', '备注', '例句']

# 全新身份，避免与既有笔记类型撞名/撞结构
model = genanki.Model(
    1748293111500,
    '无线电词汇 FR→ZH · 真题例句（含中译·原题图）',
    fields=[{'name': n} for n in FIELDS],
    templates=[{'name': '法→中 认读（真题＋中译）', 'qfmt': QFMT, 'afmt': AFMT}],
    css=CSS,
)
deck = genanki.Deck(2059400401, '法国无线电考试::词汇·真题例句（含中译·原题图）')

def tag(s):
    s = re.sub(r'[^\w\u4e00-\u9fff/]+', '_', s or '')
    return s.strip('_')[:40] or 'misc'

n_ex = n_tr = n_no = 0
for r in rows:
    fr = (r.get('Français') or '').strip()
    zhw = (r.get('中文') or '').strip()
    if not fr or not zhw:
        continue
    ex = pick(fr)
    if ex:
        n_ex += 1
        if any(zh(str(qs[i]['num']), 'stem') for i in ex):
            n_tr += 1
    else:
        n_no += 1
    deck.add_note(genanki.Note(
        model=model,
        fields=[fr, zhw, r.get('词性/类别') or '', r.get('所属主题') or '',
                r.get('频次') or '', r.get('备注') or '', render(ex, fr)],
        tags=[t for t in (tag(r.get('词性/类别', '')), tag(r.get('所属主题', ''))) if t],
        guid=genanki.guid_for('radioamateur-fr', fr),
    ))

pkg = genanki.Package(deck)
pkg.media_files = sorted(MEDIA)
pkg.write_to_file(OUT)
print()
print('词条总数     :', len(rows))
print('  有例句     :', n_ex, '（其中带中译', n_tr, '）')
print('  无例句     :', n_no)
print('  引用图片   :', len(MEDIA), '张，共 %.2f MB' % (sum(os.path.getsize(x) for x in MEDIA) / 1048576))
print('输出         :', OUT, os.path.getsize(OUT), '字节')
