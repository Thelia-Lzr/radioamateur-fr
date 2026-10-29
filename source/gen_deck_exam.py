#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把全部考题做成 Anki 卡：正面法语题+选项，背面中译+答案+官方注释+原理讲解。

数据来源
  source/Exam1/questions/questions.json     2692 道题
  source/translations_*.json                前 1135 道的中译
  source/explain/out_*.json                 前 1135 道的原理讲解
  source/full/out_*.json                    后 1557 道的中译+讲解
  source/Exam1/questions/<num>.png          原题图
用法：<venv>/bin/python gen_deck_exam.py
"""
import csv, json, os, re, html, glob
import genanki

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, 'source')
OUT = os.path.join(BASE, 'decks', '考题卡组（中译＋讲解）.apkg')
IMGDIR = os.path.join(SRC, 'Exam1', 'questions')

# ---------- 载入 ----------
qd = json.load(open(os.path.join(SRC, 'Exam1', 'questions', 'questions.json'), encoding='utf-8'))
qs = qd['questions']
themes = {str(t['num']): t['nom'] for t in qd['themes']}

THEME_ZH = {
 "Questions entrainement": "综合训练题",
 "Indicatifs d'appel français et préfixes européens": "法国呼号与欧洲前缀",
 "Transformateurs, ampli op, filtres RC LC RLC": "变压器、运算放大器、RC/LC/RLC 滤波器",
 "Antennes, couplage, propagation, ligne de transmis": "天线、耦合、传播、传输线",
 "Électricité de base": "电学基础",
 "Sanctions,  examen, perturbation, bande passante": "处罚、考试、干扰、带宽",
 "Sanctions, examen, perturbation, bande passante": "处罚、考试、干扰、带宽",
 "Définition et autorisation des classes d’émission": "发射类别的定义与授权",
 "Abréviations en code Q": "Q 简语缩写",
 "Condensateurs et bobines (séparés)": "电容与线圈（单独）",
 "Synoptiques d'émetteurs et de récepteurs": "收发信机方框图",
 "Teneur des messages, matériel obligatoire, exposition": "报文内容、强制设备、暴露防护",
 "Courants alternatifs": "交流电",
 "Diodes et transistors, classes d'amplification": "二极管、晶体管、放大类别",
 "Table d’épellation internationale": "国际字母解释法表",
 "Rôle des différents étages RF, haut-parleur, micro": "各级射频电路的作用、扬声器、话筒",
 "Gammes d’onde, décibels, CEM, protection": "波段、分贝、电磁兼容、防护",
 "Adaptation, ROS, affaiblissement linéique, calcul ": "阻抗匹配、驻波比、单位长度衰减、计算",
 "Groupements de résistances": "电阻组合",
 "Caractéristiques des antennes, longueur d'onde-fréquence": "天线特性、波长与频率",
 "Code des couleurs des résistances": "电阻色环码",
}

def theme_zh(fr):
    if fr in THEME_ZH:
        return THEME_ZH[fr]
    for k, v in THEME_ZH.items():
        if k[:35] == fr[:35]:
            return v
    return fr

# 中译：translations_*.json 与 full/out_*.json
ZH = {}
for f in glob.glob(os.path.join(SRC, 'translations_*.json')):
    ZH.update(json.load(open(f, encoding='utf-8')))
for f in [os.path.join(SRC,'full','out_%d.json'%i) for i in range(1,9) if os.path.exists(os.path.join(SRC,'full','out_%d.json'%i))]:
    ZH.update(json.load(open(f, encoding='utf-8')))

# 讲解：explain/out_*.json 是 {num: "讲解"}；full/out_*.json 是 {num: {..., "explain": "..."}}
OPTR = {}
for _f in [os.path.join(SRC,'opt','out_%d.json'%i) for i in range(1,10)]:
    if os.path.exists(_f):
        OPTR.update(json.load(open(_f, encoding='utf-8')))
print('选项译文:', len(OPTR))

# 已查证：statut A = 主要业务（题 30800 官方注释），B/C/D 教材未定义 → 只译成「地位代码」
STATUT = {'statut A': '地位代码 A', 'statut B': '地位代码 B',
          'statut C': '地位代码 C', 'statut D': '地位代码 D'}

def _auto(o):
    """数值型选项的自动「翻译」：小数逗号转点、à→至、库仑、地位代码"""
    key = o.strip().lower().rstrip('.')
    if key in STATUT:
        return STATUT[key]
    t = o.replace(' à ', ' 至 ')
    t = re.sub(r'(\d),(\d)', r'\1.\2', t)
    # 全拼单位：240 watts → 240 瓦（缩写词 MHz/kHz/Ω 不动）
    um = re.fullmatch(r'([\d.,\s]+?)\s*(ohms?|watts?|volts?|m[eè]tres?|centim[eè]tres?|amp[eè]res?|henrys?)',
                      o.strip(), re.I)
    if um:
        M = {'ohm': '欧姆', 'ohms': '欧姆', 'watt': '瓦', 'watts': '瓦', 'volt': '伏', 'volts': '伏',
             'metre': '米', 'metres': '米', 'mètre': '米', 'mètres': '米',
             'centimetre': '厘米', 'centimetres': '厘米', 'centimètre': '厘米', 'centimètres': '厘米',
             'ampere': '安培', 'amperes': '安培', 'ampère': '安培', 'ampères': '安培',
             'henry': '亨利', 'henrys': '亨利'}
        u = M.get(um.group(2).lower(), '')
        if u:
            return um.group(1).strip() + ' ' + u
    # 数字+空格+C → 库仑（电容倍数写作 2C、C/2，中间无空格，故不误伤）
    if re.fullmatch(r'[\d.,]+\s+C\s*', o):
        t = t.rstrip() + '（库仑）'
    return t

def opt_tr(o):
    """返回选项的小字译文。注意：键必须用 strip 过的形式——
    题库里部分选项带首尾空格，而译文表的键是 strip 过的。"""
    o_s = o.strip()
    key = o_s.lower().rstrip('.')
    auto = _auto(o_s).strip()
    if key in STATUT or re.fullmatch(r'[\d.,]+\s+C\s*', o_s):
        return auto          # 查证过的规则优先
    t = (OPTR.get(o_s) or '').strip()
    if not t or t == o_s:
        t = auto            # 子代理返回与原文相同 → 回退到自动规则
    return t or o_s

# ---------- 本机教材 HTML ----------
# 需要看图的题（讲解标记 + 题干图词 + 图片≥10KB）
NEEDS_IMG = set()
_ni = os.path.join(SRC, 'needs_image.json')
if os.path.exists(_ni):
    NEEDS_IMG = set(json.load(open(_ni, encoding='utf-8')))
    print('需看图的题:', len(NEEDS_IMG))

MANUEL_SRC = os.environ.get('MANUEL_OVERRIDE') or os.path.join(BASE, 'manuel-zh.html')
MANUEL_MEDIA = os.path.join(SRC, '_manuel-zh.html')   # 下划线前缀：Anki 媒体检查会跳过
if os.path.exists(MANUEL_SRC):
    import shutil
    shutil.copyfile(MANUEL_SRC, MANUEL_MEDIA)
    _m = open(MANUEL_SRC, encoding='utf-8').read()
    ANCH = set(re.findall(r'id="([^"]+)"', _m)) | set(re.findall(r'name="([^"]+)"', _m))
    print('教材锚点:', len(ANCH))
else:
    ANCH = set()
    print('警告：找不到 manuel-zh.html，链接将退回在线版')

# 题库 anchor 的已知笔误
FIXA = {'R21b)': 'R21b', 'T023ac8': 'T023c8'}

def anch_ok(a):
    a = (a or '').strip().rstrip('.')
    if a in ANCH:
        return a
    if a in FIXA and FIXA[a] in ANCH:
        return FIXA[a]
    b = a.rstrip(')').strip('.')
    return b if b in ANCH else a

def manuel_link(a):
    a = anch_ok(a)
    if not ANCH:
        return ('<a href="https://f6kgl.free.fr/COURS.html#%s">教材 §%s</a>' % (a, a))
    return '<a href="_manuel-zh.html#%s">教材 §%s（中译）</a>' % (a, a)

QVOCAB = json.load(open(os.path.join(SRC, 'q_vocab.json'), encoding='utf-8')) if os.path.exists(os.path.join(SRC, 'q_vocab.json')) else {}
print('重点词汇条目:', sum(len(v) for v in QVOCAB.values()))

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
n_zh_only = sum(1 for k, v in ZH.items() if isinstance(v, dict) and v.get('stem_zh'))
print('中译条目:', len(ZH) if not n_zh_only else n_zh_only, '| 讲解条目:', len(EXP))

MEDIA = {'法规': set(), '技术': set()}
CUR = {'k': '法规'}

# ---------- 渲染 ----------
def esc(s):
    return html.escape(str(s or ''))

def opt_list(q, rep, num=''):
    """四个选项：正确项带 data-ok；每项下方挂可显示的小字译文；末尾是按钮与重点词汇"""
    out = ['<ol class="opts">']
    for i, p in enumerate(q['propositions']):
        attr = ' data-ok="1"' if i == rep else ''
        tr = opt_tr(p)
        inner = esc(p) + '<span class="otr tr" hidden>%s</span>' % esc(tr)
        # class="tappable"：AnkiMobile 需要它才把点击传给 li（桌面端无影响）
        out.append('<li class="tappable"%s>%s</li>' % (attr, inner))
    out.append('</ol>')
    out.append('<div class="btnrow">'
               '<button id="trbtn" class="tbtn" type="button">查看翻译（C）</button>'
               '<button id="imgbtn" class="tbtn" type="button">隐藏题图（X）</button>'
               '</div>')
    fn = img_src(num) if num else ''
    show = True                        # 所有题都默认展开题图
    if fn:
        out.append('<div id="imgwrap" class="%s">'
                   '<img class="qimg" src="%s"></div>' % ('imgon' if show else 'imgoff', fn))
    v = vocab_html(num) if num else ''
    if v:
        out.append('<div class="tr vocabfront" hidden><div class="sec">重点词汇</div>%s</div>' % v)
    return ''.join(out)

def img_src(num):
    """图片文件名；存在则登记进本条牌组的媒体集"""
    fn = '%s.png' % num
    p = os.path.join(IMGDIR, fn)
    if not os.path.exists(p):
        return ''
    MEDIA[CUR['k']].add(p)
    return fn

def img_tag(num):
    """背面用：直接显示的题图"""
    fn = img_src(num)
    return '<img class="qimg" src="%s">' % fn if fn else ''


def vocab_html(num):
    """重点词汇：复用 vocabulaire.csv 里出现在本题的词"""
    v = QVOCAB.get(num) or []
    if not v:
        return ''
    out = ['<table class="vtab">']
    for w in v:
        out.append('<tr><td class="vfr">%s</td><td class="vzh">%s</td></tr>'
                   % (esc(w['fr']), esc(w['zh'])))
    out.append('</table>')
    return ''.join(out)

CSS = """
[hidden] { display:none !important; }
.card { font-family:"Noto Sans CJK SC","Source Han Sans SC",sans-serif;
  font-size:19px; color:#1c1c1c; background:#fdfdfb; padding:16px 14px;
  text-align:left; max-width:44em; margin:0 auto; }
.theme { font-size:13px; color:#8a8a8a; border-bottom:1px solid #e5e5e0;
  padding-bottom:5px; margin-bottom:10px; }
.q { font-size:21px; font-weight:600; line-height:1.45; color:#111; }
.opts { margin:12px 0 0 0; padding-left:1.6em; }
.opts li { font-size:18px; line-height:1.5; margin-bottom:4px; }
.opts li.clickable { cursor:pointer; border-radius:4px; padding:1px 6px; margin-left:-6px; }
.opts li.clickable:hover { background:#eef3f8; }
.opts li.picked-wrong { background:#fdecea; color:#b3261e; text-decoration:line-through; }
.opts li.picked-right { background:#e8f5ec; color:#1a6b34; font-weight:700; }
.otr { display:block; font-size:13px; color:#7b8fa3; font-weight:400;
  line-height:1.35; margin-top:1px; }
.opts li.picked-wrong .otr, .opts li.picked-right .otr { color:inherit; opacity:.75; }
.qtr { font-size:14px; color:#7b8fa3; margin-top:5px; }
.btnrow { margin-top:12px; display:flex; gap:8px; }
.tbtn { font-size:13px; color:#14508c; background:#eef3f8; border:1px solid #cdd8e4;
  border-radius:4px; padding:3px 10px; cursor:pointer; font-family:inherit; }
.tbtn:hover { background:#e2ebf4; }
.imgoff { display:none; }
.imgon { display:block; margin-top:10px; }
.vocabfront { margin-top:14px; }
.qzh { font-size:17px; color:#4a6b8a; line-height:1.5; margin-top:9px; }
hr#answer { border:none; border-top:2px solid #14508c; margin:14px 0; }
.ansline { font-size:19px; font-weight:700; color:#1a6b34; }
.anszh { font-size:16px; color:#1a6b34; }
.sec { font-size:14px; font-weight:700; color:#14508c; letter-spacing:.5px;
  margin:16px 0 6px; border-left:3px solid #14508c; padding-left:7px; }
.com { font-size:15px; color:#5a5a5a; font-style:italic; line-height:1.5; }
.comzh { font-size:16px; color:#333; line-height:1.6; margin-top:4px; }
.exp { font-size:17px; line-height:1.75; color:#1c1c1c; }
.exp b { color:#b3261e; }
.vtab { border-collapse:collapse; font-size:16px; margin-top:2px; }
.vtab td { padding:3px 10px 3px 0; vertical-align:top; border-bottom:1px solid #eee; }
.vtab td.vfr { font-weight:600; color:#14508c; white-space:nowrap; }
.vtab td.vzh { color:#333; }
.kp { font-size:14px; color:#666; margin-top:14px; padding-top:8px;
  border-top:1px dashed #ddd; }
.kp a { color:#14508c; text-decoration:none; }
.numid { color:#aaa; font-size:12px; }
.imgbox { margin:10px 0; }
.imgbox summary { cursor:pointer; font-size:14px; color:#14508c; font-weight:600;
  display:inline-block; padding:2px 8px; border:1px solid #cdd8e4; border-radius:4px;
  background:#eef3f8; list-style:none; }
.imgbox summary::-webkit-details-marker { display:none; }
.imgbox img { display:block; max-width:100%; height:auto; border:1px solid #d5d5d0;
  border-radius:5px; background:#fff; margin-top:6px; }
"""

FIELDS = ['题干','选项','题干中译','答案','答案中译','官方注释','注释中译',
          '原理讲解','主题','题号','锚点','图片']

QFMT = """<div class="theme">{{主题}}</div>
<div class="q">{{题干}}</div>
{{#题干中译}}<div class="qtr tr" hidden>{{题干中译}}</div>{{/题干中译}}
<div id="quiz">{{选项}}</div>
<script>
(function () {
  // ── 选项点选判对错：用事件委托，不在每个 li 上挂监听 ──
  var box = document.getElementById('quiz');
  if (box && !box.__bound) {
    box.__bound = true;
    box.addEventListener('click', function (ev) {
      var li = ev.target.closest ? ev.target.closest('ol.opts > li') : null;
      if (!li) return;
      if (li.classList.contains('picked-right')) return;
      if (li.getAttribute('data-ok') === '1') li.classList.add('picked-right');
      else li.classList.add('picked-wrong');
    });
  }

  // ── 幂等的状态设定：重复调用结果相同，不怕多个监听器 ──
  function trOn() {
    var e = document.querySelector('.tr');
    return e ? !e.hidden : false;
  }
  function setTr(on) {
    var els = document.querySelectorAll('.tr');
    for (var i = 0; i < els.length; i++) els[i].hidden = !on;
    var b = document.getElementById('trbtn');
    if (b) b.textContent = on ? '隐藏翻译（C）' : '查看翻译（C）';
  }
  function imgOn() {
    var w = document.getElementById('imgwrap');
    return w ? w.classList.contains('imgon') : false;
  }
  function setImg(on) {
    var w = document.getElementById('imgwrap');
    if (w) { w.classList.toggle('imgon', on); w.classList.toggle('imgoff', !on); }
    var b = document.getElementById('imgbtn');
    if (b) b.textContent = on ? '隐藏题图（X）' : '查看题图（X）';
  }

  // ── 按钮用 onclick 赋值（不是 addEventListener），换卡时自动覆盖，不累积 ──
  var tb = document.getElementById('trbtn');
  if (tb) {
    tb.onclick = function () { setTr(!trOn()); };
    tb.textContent = trOn() ? '隐藏翻译（C）' : '查看翻译（C）';
  }
  var ib = document.getElementById('imgbtn');
  if (ib) {
    ib.onclick = function () { setImg(!imgOn()); };
    ib.textContent = imgOn() ? '隐藏题图（X）' : '查看题图（X）';
  }

  // ── 快捷键：整个 document 只绑一次（Anki 换卡不重载页面，document 是同一个）──
  if (!window.__radioKeysBound) {
    window.__radioKeysBound = true;
    document.addEventListener('keydown', function (e) {
      // 同一个事件只处理一次：万一监听器还是重复了，也不会互相抵消
      if (e.__radioHandled) return;
      e.__radioHandled = true;
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      var t = e.target;
      if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA')) return;
      var k = e.key;
      if (k >= '1' && k <= '4') {
        var items = document.querySelectorAll('#quiz ol.opts li');
        var li = items[parseInt(k, 10) - 1];
        if (li) {
          if (!li.classList.contains('picked-right')) {
            if (li.getAttribute('data-ok') === '1') li.classList.add('picked-right');
            else li.classList.add('picked-wrong');
          }
          e.preventDefault(); e.stopPropagation();
        }
      } else if (k === 'c' || k === 'C') {
        setTr(!trOn()); e.preventDefault(); e.stopPropagation();
      } else if (k === 'x' || k === 'X') {
        setImg(!imgOn()); e.preventDefault(); e.stopPropagation();
      }
    });
  }
})();
</script>"""

AFMT = """<div class="theme">{{主题}}</div>
{{图片}}
<div class="q">{{题干}}</div>
<div class="qzh">{{题干中译}}</div>
<hr id="answer">
<div class="ansline">&#10003; {{答案}}</div>
{{#答案中译}}<div class="anszh">{{答案中译}}</div>{{/答案中译}}
{{#官方注释}}<div class="sec">官方原注</div>
<div class="com">{{官方注释}}</div>
<div class="comzh">{{注释中译}}</div>{{/官方注释}}
{{#原理讲解}}<div class="sec">原理讲解</div>
<div class="exp">{{原理讲解}}</div>{{/原理讲解}}
<div class="kp">知识点：{{主题}} &nbsp;|&nbsp;
<a href="_manuel-zh.html#{{锚点}}">教材 §{{锚点}}（中译）</a>
&nbsp;|&nbsp;<span class="numid">题号 {{题号}}</span></div>"""

model = genanki.Model(
    1748293200100,
    '法国业余无线电考题（中译·原理讲解）',
    fields=[{'name': n} for n in FIELDS],
    templates=[{'name': '考题 正/背', 'qfmt': QFMT, 'afmt': AFMT}],
    css=CSS,
)
# 两个牌组：法规与制度 / 技术原理（同一笔记类型、同一 GUID，重新导入会原地更新并移组）
DECKS = {
    '法规': genanki.Deck(2059400502, '法国无线电考试::法规与制度（中译·讲解）'),
    '技术': genanki.Deck(2059400503, '法国无线电考试::技术原理（中译·讲解）'),
}
OUTS = {
    '法规': os.path.join(BASE, 'decks', '考题卡组·法规与制度（中译＋讲解）.apkg'),
    '技术': os.path.join(BASE, 'decks', '考题卡组·技术原理（中译＋讲解）.apkg'),
}
N = {'法规': 0, '技术': 0}

def tag(s):
    s = re.sub(r'[^\w\u4e00-\u9fff/]+', '_', s or '')
    return s.strip('_')[:40] or 'misc'

n_zh = n_exp = 0
for q in qs:
    num = str(q['num'])
    rep = q['reponse']
    ans = q['propositions'][rep] if isinstance(rep, int) and 0 <= rep < len(q['propositions']) else ''
    z = ZH.get(num) or {}
    stem_zh = z.get('stem_zh') or z.get('stem') or ''
    ans_zh = z.get('ans_zh') or z.get('answer') or ''
    com_zh = z.get('com_zh') or z.get('com') or ''
    exp = EXP.get(num, '')
    if stem_zh:
        n_zh += 1
    if exp:
        n_exp += 1
    tn = themes.get(str(q['themeNum']), '')
    m = re.search(r'#(.+)$', q.get('cours') or '')
    anc = m.group(1) if m else ''
    grp = '法规' if anc.startswith('R') else '技术'
    CUR['k'] = grp
    N[grp] += 1
    DECKS[grp].add_note(genanki.Note(
        model=model,
        fields=[esc(q['question']).replace('\n', '<br>'),
                opt_list(q, rep, num),
                esc(stem_zh).replace('\n', '<br>'),
                esc(ans),
                esc(ans_zh if ans_zh.strip() != ans.strip() else ''),
                esc(str(q.get('commentaire') or '')).replace('\n', '<br>'),
                esc(com_zh).replace('\n', '<br>'),
                ((exp or '').replace('\n', '<br>')
                 + (('<div class="sec">重点词汇</div>' + vocab_html(num)) if vocab_html(num) else '')),
                '%s / %s' % (esc(tn), esc(theme_zh(tn))),
                num, anch_ok(anc), img_tag(num)],
        tags=[t for t in ('法规' if grp == '法规' else '技术', tag(theme_zh(tn))) if t],
        guid=genanki.guid_for('radioamateur-fr-exam', num),
    ))

print()
for grp in ('法规', '技术'):
    pkg = genanki.Package(DECKS[grp])
    pkg.media_files = sorted(MEDIA[grp]) + ([MANUEL_MEDIA] if os.path.exists(MANUEL_MEDIA) else [])
    pkg.write_to_file(OUTS[grp])
    print('%-4s : %4d 题 | 图片 %4d 张 %5.2f MB | %s (%.2f MB)'
          % (grp, N[grp], len(MEDIA[grp]),
             sum(os.path.getsize(x) for x in MEDIA[grp]) / 1048576,
             os.path.basename(OUTS[grp]), os.path.getsize(OUTS[grp]) / 1048576))
print()
print('题目总数   :', len(qs), '| 有中译', n_zh, '| 有讲解', n_exp)
