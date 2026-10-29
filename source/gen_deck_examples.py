#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用 Exam'1 真题给每个词条配例句，生成 Anki .apkg。
用法：<venv>/bin/python gen_deck_examples.py
"""
import csv, json, os, re, html, unicodedata
import genanki

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_CSV = os.path.join(BASE, 'data', 'vocabulaire.csv')
SRC_Q = os.path.join(BASE, 'source', 'Exam1', 'questions', 'questions.json')
OUT = os.path.join(BASE, 'decks', '无线电词汇（含真题例句）.apkg')

MAX_EX = 2          # 每个词最多几条例句
MAX_QLEN = 260      # 过长的题干跳过

# ---------- 归一化 ----------
def strip_acc(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn').lower()

def toks(s):
    return set(re.findall(r"[a-z0-9]+", strip_acc(s)))

# 允许重音变体的正则
ACC = {'a': '[aàâä]', 'e': '[eéèêë]', 'i': '[iîï]', 'o': '[oôö]',
       'u': '[uùûü]', 'c': '[cç]', 'y': '[yÿ]'}

def word_regex(w):
    out = []
    for ch in w:
        low = strip_acc(ch)
        if low.isalpha() and low in ACC:
            out.append(ACC[low])
        else:
            out.append(re.escape(ch))
    return re.compile(''.join(out), re.IGNORECASE)

def highlight(text, word):
    """把题干里的目标词加粗（允许重音/大小写差异）"""
    try:
        return word_regex(word).sub(lambda m: '<b>' + m.group(0) + '</b>', text, count=2)
    except Exception:
        return text

# ---------- 载入 ----------
rows = list(csv.DictReader(open(SRC_CSV, encoding='utf-8')))
qd = json.load(open(SRC_Q, encoding='utf-8'))
qs = qd['questions']
themes = {t['num']: t['nom'] for t in qd['themes']}

q_stem_tok, q_all_tok, q_stem_txt, q_all_txt = [], [], [], []
for q in qs:
    stem = q['question']
    full = stem + ' ' + ' '.join(q['propositions'])
    q_stem_txt.append(stem)
    q_all_txt.append(full)
    q_stem_tok.append(toks(stem))
    q_all_tok.append(toks(full))

def pick_examples(word, limit=MAX_EX):
    """挑最合适的例句：优先题干命中、短句、带官方注释"""
    w_norm = strip_acc(word)
    single = len(re.findall(r"[a-z0-9]+", w_norm)) == 1
    scored = []
    for i, q in enumerate(qs):
        if single:
            if w_norm not in q_all_tok[i]:
                continue
            in_stem = w_norm in q_stem_tok[i]
        else:
            if w_norm not in strip_acc(q_all_txt[i]):
                continue
            in_stem = w_norm in strip_acc(q_stem_txt[i])
        L = len(q_all_txt[i])
        if L > MAX_QLEN:
            continue
        score = (3 if in_stem else 0) + (1 if q.get('commentaire') else 0) - L / 400.0
        scored.append((score, i))
    scored.sort(reverse=True)
    return [qs[i] for _, i in scored[:limit]]

def render(examples, word):
    if not examples:
        return ''
    parts = ['<div class="exwrap"><div class="extitle">真题例句</div>']
    for q in examples:
        raw = q['question']
        marked = highlight(raw, word)          # 先加粗
        esc = html.escape(marked).replace('&lt;b&gt;', '<b>').replace('&lt;/b&gt;', '</b>')
        rep = q['reponse']
        ans = q['propositions'][rep] if isinstance(rep, int) and 0 <= rep < len(q['propositions']) else ''
        parts.append('<div class="ex">')
        parts.append('<div class="exq">%s</div>' % esc)
        if ans:
            parts.append('<div class="exa">&#10003; %s</div>' % html.escape(ans))
        if q.get('commentaire'):
            parts.append('<div class="exc">%s</div>' % html.escape(str(q['commentaire'])))
        parts.append('</div>')
    parts.append('</div>')
    return ''.join(parts)

# ---------- 生成 ----------
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
.ex { background:#f4f6f2; border-left:3px solid #14508c; padding:8px 12px; margin-bottom:8px; border-radius:0 6px 6px 0; }
.exq { font-size:17px; line-height:1.45; color:#222; }
.exq b { color:#b3261e; }
.exa { font-size:16px; color:#1a6b34; margin-top:5px; font-weight:600; }
.exc { font-size:14px; color:#666; margin-top:5px; font-style:italic; line-height:1.4; }
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

model = genanki.Model(
    1748293077700,
    '无线电词汇 FR→ZH · 含真题例句',
    fields=[{'name': n} for n in FIELDS],
    templates=[{'name': '法→中 认读（含真题）', 'qfmt': QFMT, 'afmt': AFMT}],
    css=CSS,
)
deck = genanki.Deck(2059400199, '法国无线电考试::词汇·含真题例句')

def tag(s):
    s = re.sub(r'[^\w\u4e00-\u9fff/]+', '_', s or '')
    return s.strip('_')[:40] or 'misc'

with_ex = no_ex = 0
for r in rows:
    fr = (r.get('Français') or '').strip()
    zh = (r.get('中文') or '').strip()
    if not fr or not zh:
        continue
    ex = pick_examples(fr)
    if ex:
        with_ex += 1
    else:
        no_ex += 1
    deck.add_note(genanki.Note(
        model=model,
        fields=[fr, zh, r.get('词性/类别') or '', r.get('所属主题') or '',
                r.get('频次') or '', r.get('备注') or '', render(ex, fr)],
        tags=[t for t in (tag(r.get('词性/类别', '')), tag(r.get('所属主题', ''))) if t],
        guid=genanki.guid_for('radioamateur-fr', fr),
    ))

genanki.Package(deck).write_to_file(OUT)
print('词条总数 :', len(rows))
print('  带例句 :', with_ex)
print('  无例句 :', no_ex)
print('输出     :', OUT, os.path.getsize(OUT), '字节')
