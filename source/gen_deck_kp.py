#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把知识点做成 Anki 复习卡：正面一个提问，背面完整讲解 + 中法对照例题 + 例题原图。

数据来源
  source/kp_list.json          120 个知识点（主题/锚点/章节/覆盖题号）
  source/kp/out_*.json         写手产出的标题/提问/讲解
  source/Exam1/questions/*.png 原题图
用法：<venv>/bin/python gen_deck_kp.py
"""
import json, os, re, html, glob
import genanki

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, 'source')
OUT = os.path.join(BASE, 'decks', '知识卡组（法国特色法规）.apkg')
IMGDIR = os.path.join(SRC, 'Exam1', 'questions')

# ---------- 载入 ----------
kps = json.load(open(os.path.join(SRC, 'kp_list.json'), encoding='utf-8'))
qd = json.load(open(os.path.join(SRC, 'Exam1', 'questions', 'questions.json'), encoding='utf-8'))
Q = {str(q['num']): q for q in qd['questions']}

MANUEL_SRC = os.environ.get('MANUEL_OVERRIDE') or os.path.join(BASE, 'manuel-zh.html')
MANUEL_MEDIA = os.path.join(SRC, '_manuel-zh.html')
if os.path.exists(MANUEL_SRC):
    import shutil
    shutil.copyfile(MANUEL_SRC, MANUEL_MEDIA)
    _m = open(MANUEL_SRC, encoding='utf-8').read()
    ANCH = set(re.findall(r'id="([^"]+)"', _m)) | set(re.findall(r'name="([^"]+)"', _m))
    print('教材锚点:', len(ANCH))
else:
    ANCH = set()

FIXA = {'R21b)': 'R21b', 'T023ac8': 'T023c8'}

def anch_ok(a):
    a = (a or '').strip().rstrip('.')
    if a in ANCH: return a
    if a in FIXA and FIXA[a] in ANCH: return FIXA[a]
    b = a.rstrip(')').strip('.')
    return b if b in ANCH else a

KP = {}
for f in glob.glob(os.path.join(SRC, 'kp', 'out_*.json')):
    KP.update(json.load(open(f, encoding='utf-8')))
print('知识点:', len(kps), '| 已写:', len(KP))

# 应用合并结果：被合并掉的 id 不再单独出卡，保留者用合并后的正文
MERGED = os.path.join(SRC, 'kp', 'merged_out.json')
DROP = set()
if os.path.exists(MERGED):
    for g, v in json.load(open(MERGED, encoding='utf-8')).items():
        if not isinstance(v, dict):
            continue
        if v.get('title_zh') == 'KEEP_SEPARATE':
            print('  [合并] %s 判定为不同知识点，保持独立' % g)
            continue
        keep = v.get('keep_id')
        drops = v.get('drop_ids') or []
        if keep and keep in KP and v.get('body'):
            KP[keep] = {'title_fr': v.get('title_fr', ''),
                        'title_zh': v.get('title_zh') or KP[keep].get('title_zh', ''),
                        'front': v.get('front') or KP[keep].get('front', ''),
                        'body': v['body']}
            DROP.update(drops)
            print('  [合并] %s → 保留 %s，合并掉 %s' % (g, keep, drops))
if DROP:
    # 被合并掉的点的题号要并进保留者，否则例题与原题图会丢
    by_id = {p['id']: p for p in kps}
    for g, v in json.load(open(MERGED, encoding='utf-8')).items():
        if not isinstance(v, dict) or v.get('title_zh') == 'KEEP_SEPARATE':
            continue
        keep, drops = v.get('keep_id'), (v.get('drop_ids') or [])
        if keep in by_id:
            extra = []
            for d in drops:
                if d in by_id:
                    extra += [n for n in by_id[d]['nums'] if n not in by_id[keep]['nums']]
            if extra:
                by_id[keep]['nums'] = by_id[keep]['nums'] + extra
                by_id[keep]['n'] = len(by_id[keep]['nums'])
                print('  [合并] %s 并入 %d 道例题题号' % (keep, len(extra)))
    kps = [p for p in kps if p['id'] not in DROP]
    print('  合并后知识点总数:', len(kps))

# 中译（用于例题对照）
ZH = {}
for f in glob.glob(os.path.join(SRC, 'translations_*.json')):
    ZH.update(json.load(open(f, encoding='utf-8')))
for f in [os.path.join(SRC,'full','out_%d.json'%i) for i in range(1,9) if os.path.exists(os.path.join(SRC,'full','out_%d.json'%i))]:
    ZH.update(json.load(open(f, encoding='utf-8')))
EXP = {}
for f in glob.glob(os.path.join(SRC, 'explain', 'out_*.json')):
    for k, v in json.load(open(f, encoding='utf-8')).items():
        if isinstance(v, str):
            EXP[k] = v
        elif isinstance(v, dict) and v.get('explain'):
            EXP[k] = v['explain']
for f in [os.path.join(SRC,'full','out_%d.json'%i) for i in range(1,9) if os.path.exists(os.path.join(SRC,'full','out_%d.json'%i))]:
    for k, v in json.load(open(f, encoding='utf-8')).items():
        if isinstance(v, dict) and v.get('explain'):
            EXP[k] = v['explain']

def zh_of(num, *keys):
    v = ZH.get(num) or {}
    if not isinstance(v, dict):
        return ''
    for k in keys:
        if v.get(k):
            return v[k]
    return ''

MEDIA = set()

# ---------- 轻量标记 → HTML ----------
def md2html(t):
    r"""支持：## 小标题 / - 列表 / **粗体** / \( \) \[ \] / 空行分段"""
    t = (t or '').replace('\r', '')
    out, in_ul = [], False
    for raw in t.split('\n'):
        line = raw.rstrip()
        if not line.strip():
            if in_ul:
                out.append('</ul>'); in_ul = False
            continue
        body = html.escape(line.strip())
        # 还原 LaTeX 与粗体（html.escape 会把它们转义）
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

# ---------- 例题 ----------
def example_block(p, k=4):
    """中法对照例题 + 原题图"""
    nums = p['nums']
    # 优先带官方注释、题干较短的，且尽量带图
    qs = [Q[n] for n in nums if n in Q]
    def key(q):
        return (0 if q.get('commentaire') else 1,
                len(q['question']) + len(' '.join(q['propositions'])))
    qs.sort(key=key)
    out = ['<div class="exwrap"><div class="extitle">中法对照例题</div>']
    for q in qs[:k]:
        num = str(q['num'])
        rep = q['reponse']
        ans = q['propositions'][rep] if isinstance(rep, int) and 0 <= rep < len(q['propositions']) else ''
        out.append('<div class="ex">')
        img = '%s.png' % num
        if os.path.exists(os.path.join(IMGDIR, img)):
            MEDIA.add(os.path.join(IMGDIR, img))
            out.append('<details class="imgbox"><summary>原题图</summary><img src="%s"></details>' % img)
        out.append('<div class="exfr">%s</div>' % html.escape(q['question']))
        tz = zh_of(num, 'stem_zh', 'stem')
        if tz:
            out.append('<div class="exzh">%s</div>' % html.escape(tz))
        opts = []
        for i, o in enumerate(q['propositions']):
            opts.append('<li class="%s">%s</li>' % ('ok' if i == rep else '', html.escape(o)))
        out.append('<ol class="exopts">%s</ol>' % ''.join(opts))
        if ans:
            az = zh_of(num, 'ans_zh', 'answer')
            out.append('<div class="exans">&#10003; %s%s</div>' %
                       (html.escape(ans), ('　' + html.escape(az)) if az and az.strip() != ans.strip() else ''))
        ex = EXP.get(num, '')
        if ex:
            out.append('<details class="exdet"><summary>为什么</summary><div class="exexp">%s</div></details>'
                       % html.escape(ex).replace('\n', '<br>'))
        out.append('</div>')
    out.append('</div>')
    return ''.join(out)

# ---------- 模板 ----------
CSS = """
.card { font-family:"Noto Sans CJK SC","Source Han Sans SC",sans-serif;
  font-size:19px; color:#1c1c1c; background:#fdfdfb; padding:18px 16px;
  text-align:left; max-width:46em; margin:0 auto; line-height:1.7; }
.tag { font-size:12px; color:#8a8a8a; border-bottom:1px solid #e5e5e0;
  padding-bottom:5px; margin-bottom:12px; }
.front-fr { font-size:15px; color:#7a7a7a; font-style:italic; margin-bottom:6px; }
.front-q { font-size:23px; font-weight:600; line-height:1.5; color:#111; }
h2.kf { font-size:24px; color:#14508c; margin:0 0 4px; line-height:1.4; }
h2.kz { font-size:19px; color:#333; font-weight:600; margin:0 0 14px; }
hr#answer { border:none; border-top:2px solid #14508c; margin:16px 0; }
.h4 { font-size:17px; font-weight:700; color:#14508c; margin:16px 0 6px;
  border-left:3px solid #14508c; padding-left:8px; }
.p { margin:7px 0; }
.ul { margin:7px 0 7px 1.4em; padding:0; }
.ul li { margin:3px 0; }
.body b { color:#b3261e; }
.exwrap { margin:22px 0 0; padding-top:12px; border-top:2px dashed #cfd8e0; }
.extitle { font-size:16px; font-weight:700; color:#333; margin-bottom:9px; }
.ex { background:#f4f6f2; border-left:3px solid #14508c; padding:9px 12px;
  margin-bottom:11px; border-radius:0 6px 6px 0; }
.exfr { font-size:15px; color:#222; line-height:1.5; }
.exzh { font-size:14px; color:#4a6b8a; line-height:1.5; margin-top:3px; }
.exopts { margin:6px 0 0 1.5em; padding:0; font-size:14px; color:#444; }
.exopts li { margin:1px 0; }
.exopts li.ok { color:#1a6b34; font-weight:700; }
.exans { font-size:14px; color:#1a6b34; font-weight:700; margin-top:5px; }
.exdet { margin-top:6px; }
.exdet summary { cursor:pointer; font-size:13px; color:#14508c; font-weight:600; }
.exexp { font-size:13px; color:#555; line-height:1.6; margin-top:4px;
  border-top:1px dashed #ccc; padding-top:5px; }
.imgbox { margin:0 0 7px; }
.imgbox summary { cursor:pointer; font-size:13px; color:#14508c; font-weight:600;
  display:inline-block; padding:2px 8px; border:1px solid #cdd8e4; border-radius:4px;
  background:#eef3f8; list-style:none; }
.imgbox summary::-webkit-details-marker { display:none; }
.imgbox img { display:block; max-width:100%; height:auto; border:1px solid #d5d5d0;
  border-radius:5px; background:#fff; margin-top:6px; }
.foot { font-size:12px; color:#999; margin-top:16px; padding-top:8px;
  border-top:1px dashed #ddd; }
.foot a { color:#14508c; text-decoration:none; }
"""

FIELDS = ['知识点','法语标题','正面提问','讲解','主题','锚点','题号','例题']

QFMT = """<div class="tag">{{主题}}</div>
<div class="front-fr">{{法语标题}}</div>
<div class="front-q">{{正面提问}}</div>"""

AFMT = """<div class="tag">{{主题}}</div>
<h2 class="kf">{{法语标题}}</h2>
<h2 class="kz">{{知识点}}</h2>
<hr id="answer">
<div class="body">{{讲解}}</div>
{{例题}}
<div class="foot">教材 <a href="_manuel-zh.html#{{锚点}}">§{{锚点}}（中译）</a>
&nbsp;|&nbsp;{{题号}}</div>"""

model = genanki.Model(
    1748293300100,
    '法国业余无线电知识点（法规·中法例题）',
    fields=[{'name': n} for n in FIELDS],
    templates=[{'name': '知识点 提问/复习', 'qfmt': QFMT, 'afmt': AFMT}],
    css=CSS,
)
deck = genanki.Deck(2059400601, '法国无线电考试::知识点（中法对照例题）')

def tag(s):
    s = re.sub(r'[^\w\u4e00-\u9fff/]+', '_', s or '')
    return s.strip('_')[:40] or 'misc'

n_ok = 0
for p in kps:
    d = KP.get(p['id']) or {}
    title_zh = (d.get('title_zh') or '').strip() or p['theme_zh']
    title_fr = (d.get('title_fr') or '').strip() or p['anchor']
    front = (d.get('front') or '').strip() or ('请复习：%s' % title_zh)
    body = md2html(d.get('body') or '')
    if body:
        n_ok += 1
    deck.add_note(genanki.Note(
        model=model,
        fields=[title_zh, html.escape(title_fr), html.escape(front), body,
                '%s · §%s' % ('法国/欧盟规章' if p['anchor'].startswith('R') else '技术原理',
                              p['anchor'].strip('.') or '—'),
                anch_ok(p['anchor']),
                '%d 道相关真题' % p['n'], example_block(p)],
        tags=[t for t in ('法规' if p['anchor'].startswith('R') else '技术',
                          '§%s' % p['anchor'].strip('.') if p['anchor'].strip('.') else '',
                          tag(title_zh)) if t],
        guid=genanki.guid_for('radioamateur-fr-kp', p['id'], title_zh),
    ))

pkg = genanki.Package(deck)
pkg.media_files = sorted(MEDIA) + ([MANUEL_MEDIA] if os.path.exists(MANUEL_MEDIA) else [])
pkg.write_to_file(OUT)
print()
print('知识点卡片   :', len(kps))
print('  有讲解正文 :', n_ok)
print('  引用例题图 :', len(MEDIA), '张 %.2f MB' % (sum(os.path.getsize(x) for x in MEDIA) / 1048576))
print('输出         :', OUT, os.path.getsize(OUT), '字节')
