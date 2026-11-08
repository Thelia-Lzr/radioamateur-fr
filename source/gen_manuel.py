#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Assemble manuel-zh.html : manuel chinois de preparation au certificat
# d'operateur du service amateur (d'apres le COURS de F6KGL, CC BY-NC-SA 4.0).
import importlib, json, os, re, html, sys, collections
from gen_common import (load_questions, questions_by_anchor, norm_anchor,
                        theme_names, count_section)
from manual_quiz import QUIZ_CSS, QUIZ_SCRIPT, render_question
from study_polish import polish_document
from lesson_vocab import add_lesson_vocab
from all_lesson_questions import add_all_lesson_questions
from learning_supplements import add_learning_supplements

BASE = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.abspath(os.path.join(BASE, '..', 'manuel-zh.html'))
BLOCKS = ['W1', 'W2', 'W3', 'W4', 'W4b', 'W5', 'W6', 'W7', 'W8', 'W9', 'W10', 'W11']

CHAPTERS = [
    ('R-1', '法规 R-1　监管框架、发射类别与使用条件'),
    ('R-2', '法规 R-2　频率划分与功率'),
    ('R-3', '法规 R-3　国际字母解释法、Q 简语与考试'),
    ('R-4', '法规 R-4　呼号、操作许可、处罚与台站管理'),
    ('R-5', '法规 R-5　法规卷里的技术基础'),
    ('T-0', '技术 0　数学与单位基础'),
    ('T-1', '技术 1　电学基础'),
    ('T-2', '技术 2　交流电、电容与线圈'),
    ('T-3', '技术 3　变压器、电源与测量'),
    ('T-4', '技术 4　分贝与滤波电路'),
    ('T-5', '技术 5　二极管与电源电路'),
    ('T-6', '技术 6　晶体管与电子管'),
    ('T-7', '技术 7　放大器、振荡器与混频器'),
    ('T-8', '技术 8　运算放大器与数字逻辑'),
    ('T-9', '技术 9　天线与传播'),
    ('T-10', '技术 10　传输线、驻波与匹配'),
    ('T-11', '技术 11　接收机与发射机框图'),
    ('T-12', '技术 12　调制方式（AM / FM / CW / BLU）与占用带宽'),
]


def chapter_of(section):
    if section.startswith('R'):
        return 'R-%s' % section[1]
    return 'T-%d' % int(section[1:3])


def load_content():
    sections, qt = [], {}
    for name in BLOCKS:
        try:
            m = importlib.import_module('content_' + name)
        except ImportError as e:
            print('!! module manquant : content_%s (%s)' % (name, e))
            continue
        sections.extend(getattr(m, 'SECTIONS', []))
        qt.update(getattr(m, 'QT', {}))
    return sections, qt


def load_extra(mod):
    try:
        m = importlib.import_module(mod)
        return m
    except ImportError as e:
        print('!! module manquant : %s (%s)' % (mod, e))
        return None


def esc(s):
    return html.escape(s, quote=False)


def fr_text(s):
    # texte francais d'une question (retours a la ligne -> <br>)
    return '<br>'.join(esc(x) for x in s.split('\n'))


def question_options(q):
    """Show the source choices without revealing which one is correct."""
    out = ['<p class="small question-number">Exam\'1 题号：%s · 单选</p>'
           % esc(str(q['num'])),
           '<ol class="exam-options" type="A" lang="fr" data-question="%s">'
           % html.escape(str(q['num']), quote=True)]
    for choice in q['propositions']:
        out.append('<li class="fr">%s</li>' % fr_text(choice))
    out.append('</ol>')
    return '\n'.join(out)


TAG = re.compile(r'<(/?)(li|ul|ol|table|tr|td|th|div|p|details|summary)\b[^>]*>', re.I)


def fix_li(body):
    # referme les <li> laisses ouverts par les redacteurs
    out, open_li, pos = [], 0, 0
    for m in TAG.finditer(body):
        out.append(body[pos:m.start()])
        pos = m.end()
        close, name = m.group(1) == '/', m.group(2).lower()
        if name == 'li':
            if close:
                open_li = max(0, open_li - 1)
            else:
                open_li += 1
        elif name in ('ul', 'ol') and close and open_li:
            out.append('</li>' * open_li)
            open_li = 0
        out.append(m.group(0))
    out.append(body[pos:])
    if open_li:
        out.append('</li>' * open_li)
    return ''.join(out)


def clean_title(t, ref):
    # evite « §R-2.1 §R-2.1 总览... » quand le redacteur a repris la reference
    t = (t or '').strip()
    for pre in ('§' + ref, ref, '§' + ref.replace('-', '')):
        if t.lower().startswith(pre.lower()):
            t = t[len(pre):].lstrip('　 :：·-')
            break
    return t or (ref and '§' + ref) or ''


def order_key(u):
    # dans une section : unite generale d'abord, puis les signets a, b, c...
    ref = u['ref']
    signet = ref.rsplit('.', 1)[-1] if ref.count('.') >= 2 else ''
    if signet and not signet[0].isalpha():
        signet = ''
    return (u['line'], 0 if u['main'] else 1, signet)


CSS = """
:root { --ink:#1c1c1c; --sub:#555; --line:#c9c9c4; --bg:#fdfdfb; --box:#f4f6f2; }
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { margin:0; background:var(--bg); color:var(--ink);
  font-family: "Noto Sans CJK SC","Source Han Sans SC","PingFang SC","Microsoft YaHei",
    "Hiragino Sans GB",-apple-system,"Segoe UI",sans-serif;
  font-size:16.5px; line-height:1.78; }
main { max-width: 980px; margin: 0 auto; padding: 1.2rem 1.15rem 6rem; }
h1 { font-size:1.75rem; line-height:1.4; margin:.2rem 0 .3rem; }
h2 { font-size:1.3rem; margin:2.6rem 0 .8rem; padding:.35rem .1rem .35rem .6rem;
  border-left:5px solid #4a6b8a; background:#eef2f6; }
h3 { font-size:1.1rem; margin:1.9rem 0 .55rem; padding-bottom:.25rem;
  border-bottom:1px solid var(--line); }
h3 .anch { font-size:.78rem; font-weight:400; color:#7a6a4a; margin-left:.5rem;
  font-family: ui-monospace,Menlo,Consolas,monospace; white-space:nowrap; }
h4 { font-size:1rem; margin:1.2rem 0 .4rem; }
p { margin:.55rem 0; }
ul,ol { margin:.5rem 0 .5rem 1.3rem; padding:0; }
li { margin:.25rem 0; }
code, .formula { font-family: ui-monospace,"DejaVu Sans Mono",Menlo,Consolas,monospace; }
code { background:#f0f0ec; padding:.05em .3em; border-radius:3px; font-size:.94em; }
.formula { background:#f7f7f2; border:1px solid var(--line); border-radius:4px;
  padding:.55rem .8rem; margin:.6rem 0; white-space:pre-wrap; font-size:.95rem; }
table { border-collapse:collapse; width:100%; margin:.7rem 0; font-size:.94rem; }
th,td { border:1px solid #b7b7ae; padding:.34rem .5rem; text-align:left;
  vertical-align:top; }
th { background:#e3e9f0; font-weight:600; border-bottom:2px solid #9aa8b5; }
tbody tr:nth-child(even) { background:#f7f8f6; }
.lead { color:var(--sub); font-size:.95rem; }
.toc { background:var(--box); border:1px solid var(--line); border-radius:5px;
  padding:.7rem 1rem .9rem; margin:1.2rem 0; }
.toc h2 { margin-top:.4rem; background:none; border:none; padding:0; font-size:1.1rem; }
.toc ol { list-style:none; margin-left:0; }
.toc ol ol { margin-left:1.2rem; }
.toc li { margin:.12rem 0; }
.toc a { text-decoration:none; color:#28496b; }
.toc a:hover { text-decoration:underline; }
.toc .n { color:#8a8a82; font-size:.82em; }
.exam { border:1px solid #b9c6d2; border-left:5px solid #4a6b8a; background:#f4f7fa;
  border-radius:4px; padding:.6rem .9rem .7rem; margin:1rem 0 1.4rem; }
.exam .hd { font-weight:600; margin:.1rem 0 .5rem; }
.exam ol { margin-left:1.4rem; }
.exam li { margin:.6rem 0; }
.exam .exam-options { margin:.5rem 0 .8rem 1.8rem; list-style-type:upper-alpha; }
.exam .exam-options > li { padding:.25rem .5rem; margin:.25rem 0;
  background:#fff; border:1px solid #d7dfe7; border-radius:3px;
  overflow-wrap:anywhere; }
.exam .exam-options > li::marker { font-weight:600; color:#28496b; }
.exam .question-number { margin:.3rem 0; }
.fr { font-family: Georgia,"Times New Roman",serif; color:#3a3a3a; }
.zh { color:#1c1c1c; }
details { margin:.25rem 0 0; }
summary { cursor:pointer; color:#2f5d3a; font-size:.92rem; }
.ans { margin:.3rem 0 0; padding:.35rem .6rem; background:#eef5ee;
  border-left:3px solid #6a9a72; font-size:.95rem; }
.note { background:#f6f6f0; border-left:4px solid #b9b09a; padding:.5rem .8rem;
  margin:.7rem 0; }
.warn { background:#fdf6e3; border-left:4px solid #d9a441; padding:.5rem .8rem;
  margin:.7rem 0; }
.tips { background:#eef5ee; border-left:4px solid #6a9a72; padding:.5rem .8rem;
  margin:.7rem 0; }
.facts td:first-child { width:40%; }
.anchindex td, .anchindex th { font-size:.9rem; }
.small { font-size:.88rem; color:var(--sub); }
hr { border:none; border-top:1px solid var(--line); margin:2rem 0; }
@media print { body { font-size:11pt; } .toc { page-break-after:always; } }
@media (max-width: 760px) { table { display:block; overflow-x:auto; white-space:normal; } }
.exam .fr { font-size:.96rem; }
"""
CSS += QUIZ_CSS


def build(units, sections, qt, plan):
    # fusion plan + contenu redige
    by_id = {u['id']: u for u in units}
    have = {s['id'] for s in sections}
    missing = [u['id'] for u in units if u['id'] not in have]
    extra = [s['id'] for s in sections if s['id'] not in by_id]
    units_sorted = sorted(units, key=order_key)
    order = {u['id']: i for i, u in enumerate(units_sorted)}
    # les unites sans texte redige recoivent un corps de remplacement
    for u in units:
        if u['id'] in have:
            continue
        sections.append({'id': u['id'], 'ref': u['ref'],
                         'title_zh': u['title_fr'] or '（未撰写）',
                         'title_fr': u['title_fr'],
                         'body': '<div class="warn">⚠️ 待核实：本节正文尚未撰写'
                                 '（原计划的撰写分块 %s）。可先参考法文原文 §%s。</div>'
                                 % (u.get('block', '?'), u['ref'])})
    sections = [s for s in sections if s['id'] in by_id]
    sections.sort(key=lambda s: order[s['id']])
    if missing:
        print('!! unites sans texte (%d) : %s' % (len(missing), ', '.join(missing[:40])))
    if extra:
        print('!! unites en trop (ignorees) : %s' % ', '.join(extra[:40]))

    # chapitres
    chap = collections.OrderedDict()
    for key, title in CHAPTERS:
        chap[key] = {'title': title, 'units': []}
    for s in sections:
        u = by_id[s['id']]
        key = chapter_of(u['section'])
        if key in chap:
            chap[key]['units'].append(s)

    out = []
    A = out.append
    A('<!DOCTYPE html>')
    A('<html lang="zh-CN"><head><meta charset="utf-8">')
    A('<meta name="viewport" content="width=device-width, initial-scale=1">')
    A('<title>法国业余无线电操作员证书备考教材（中文版）</title>')
    A('<style>%s</style></head><body><main>' % CSS)

    # ---------------------------------------------------------------- couverture
    A('<h1>法国业余无线电操作员证书备考教材（中文版）</h1>')
    A('<p class="lead">Certificat d\'opérateur du service amateur — 法国业余无线电操作员证书'
      '（CEPT/HAREC 级别·单一等级）· 基于 F6KGL《COURS》整理</p>')
    A('<div class="note"><b>本教材是什么：</b>把法国最主流的免费备考教材（F6KGL 的《COURS》，'
      '2025 年 11 月版）逐章改写为中文，并按 Exam\'1 题库（2692 道真题）的实际题目分布'
      '标出每节的题量与典型考法。你可以一边读中文讲解，一边用 <code>Exam1/questions/questions.json</code>'
      '里的法语原题练习。<br><b>本教材不是什么：</b>不是官方文件，不能替代 ANFR 公布的'
      '考试大纲与法规原文。凡有疑义，以 ANFR / 官方 <i>arrêté</i> 为准。</div>')

    # ---------------------------------------------------------------- sommaire
    A('<div class="toc">')
    A('<h2>目录</h2>')
    A('<ol>')
    for key, c in chap.items():
        if not c['units']:
            continue
        n = sum(by_id[s['id']]['nq'] for s in c['units'])
        A('<li><a href="#chap-%s">%s</a> <span class="n">（相关真题 %d 道）</span>' % (key, esc(c['title']), n))
        A('<ol>')
        for s in c['units']:
            u = by_id[s['id']]
            tz = clean_title(s.get('title_zh'), s.get('ref', u['ref']))
            A('<li><a href="#%s">§%s %s</a> <span class="n">（%d 题）</span></li>'
              % (s['id'], esc(s.get('ref', u['ref'])), esc(tz), u['nq']))
        A('</ol></li>')
    A('<li><a href="#annexes">附录</a>：考试战术 · 公式速查 · Q 简语 · 字母解释法 · 高频词汇 · '
      '章节权重 · 待核实清单</li>')
    A('</ol></div>')

    # ---------------------------------------------------------------- avant-propos
    front = load_extra('content_front')
    if front:
        A(front.render(by_id, units))

    # ---------------------------------------------------------------- corps
    warns = []
    for key, c in chap.items():
        if not c['units']:
            continue
        A('<h2 id="chap-%s">%s</h2>' % (key, esc(c['title'])))
        for s in c['units']:
            u = by_id[s['id']]
            tz = clean_title(s.get('title_zh'), s.get('ref', u['ref']))
            A('<h3 id="%s">§%s　%s' % (s['id'], esc(s.get('ref', u['ref'])), esc(tz)))
            anch = [a for a in (u.get('anchors') or []) if a != s['id']]
            if s.get('title_fr'):
                A('<span class="small"> · %s</span>' % esc(s['title_fr'][:70]))
            A('<span class="anch">#%s</span>' % s['id'])
            for a in anch:
                A('<span class="anch" id="%s">#%s</span>' % (a, a))
            A('</h3>')
            body = (s.get('body') or '').strip()
            body = fix_li(body)
            for w in re.findall(r'<div class="warn">(.*?)</div>', body, re.S):
                warns.append((s.get('ref', ''), re.sub(r'<[^>]+>', '', w).strip()))
            A(body)
            # --- encadre questions d'examen
            picks = u.get('picks') or []
            if picks:
                A('<div class="exam">')
                A('<div class="hd">高频考点：本节相关真题共 %d 道，下面示例 %d 道'
                  '（默认显示法语、选项与题图；翻译、词汇和答案按需查看）</div>' % (u['nq'], len(picks)))
                A('<p class="quiz-navigation-help">点击题框选中；方向键切换题目，'
                  '1–4 选择答案，C 查看本题翻译与词汇，X 切换本题题图，Z 展开本题解析。</p>')
                A('<ol>')
                for q in picks:
                    zh = qt.get(q['num'])
                    answer = ('<p class="ans">✔ 正确答案：%s — <span class="fr">%s</span>'
                              % (chr(ord('A') + q['reponse']),
                                 fr_text(q['propositions'][q['reponse']])))
                    if zh and len(zh) > 1:
                        answer += '　→　%s' % esc(zh[1])
                    answer += '</p>'
                    A(render_question(q, 'quiz-%s-%s' % (s['id'], q['num']),
                                      translation_html=esc(zh[0]) if zh else None,
                                      answer_html=answer))
                A('</ol>')
                A('<p class="small">题号为 Exam\'1 题库中的 <code>num</code>；'
                  '全部选项已按题库原顺序列出，先作答，再展开查看答案。</p>')
                A('</div>')
            elif u['nq'] == 0:
                A('<div class="exam"><div class="hd">高频考点</div>'
                  '<p class="small">本题库（2692 道）中没有直接对应本节签的真题；'
                  '本节按大纲保留，读懂即可，不必投入过多时间。</p></div>')

    # ---------------------------------------------------------------- annexes
    back = load_extra('content_back')
    if back:
        A(back.render(by_id, units, warns, qt))
    A('</main><script id="manual-quiz-script">%s</script></body></html>' % QUIZ_SCRIPT)
    document, _ = polish_document('\n'.join(out))
    document = add_lesson_vocab(document)
    document = add_all_lesson_questions(document, units)
    document = add_learning_supplements(document, units)
    return document, warns


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate a draft of the Chinese study manual.')
    parser.add_argument('--output', default=DEST, help='Output HTML path (default: manuel-zh.html).')
    args = parser.parse_args()
    plan = json.load(open(os.path.join(BASE, 'plan.json'), encoding='utf-8'))
    units = plan['units']
    sections, qt = load_content()
    doc, warns = build(units, sections, qt, plan)
    destination = os.path.abspath(args.output)
    with open(destination, 'w', encoding='utf-8') as output:
        output.write(doc)
    nq = sum(u['nq'] for u in units)
    print('-> %s (%.1f Ko, %d sections, %d questions couvertes, %d avertissements)'
          % (destination, len(doc.encode('utf-8')) / 1024.0, len(sections), nq, len(warns)))


if __name__ == '__main__':
    main()
