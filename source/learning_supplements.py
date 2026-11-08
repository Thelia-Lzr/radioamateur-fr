"""Render sourced vocabulary, chapter memory maps, and the alphabetical appendix."""
import html
import json
from pathlib import Path
import re
from gen_common import section_questions
from manual_quiz import card_content, text_html
from build_learning_vocab import key

BASE = Path(__file__).resolve().parent

def data(name):
    return json.loads((BASE / name).read_text(encoding='utf-8'))

def esc(value):
    return html.escape(str(value))

def question_link(sid, number):
    return f'<a href="#review-{sid}-{number}">题 {number}</a>'

def expanded_vocabulary(sid):
    original = data('lesson_vocab.json')[sid]
    sourced = data('question_vocab.json')[sid]
    rows = []
    seen = set()
    for entry in sourced:
        seen.add(key(entry['fr']))
        refs = '、'.join(question_link(sid, n) for n in entry['questions'][:2])
        rows.append(f'<li><span lang="fr">{esc(entry["fr"])}</span>：{esc(entry["zh"])}'
                    f'<small>〔{esc(entry["category"])} · {refs}〕</small></li>')
    for fr,zh in original:
        if key(fr) not in seen:
            rows.append(f'<li><span lang="fr">{esc(fr)}</span>：{esc(zh)}<small>〔正文基础术语〕</small></li>')
    return (f'<aside class="lesson-vocab" data-section="{sid}" aria-label="本节必备法语词汇">'
            '<p>本节必备法语词汇</p><p class="vocab-help">取自本节题干与选项；点击题号可核对语境。动词保留题中形式或注明不定式。</p>'
            '<ul>' + ''.join(rows) + '</ul></aside>')

CSS = '''<style id="learning-supplement-style">
.memory-card { border:2px solid #216870; border-radius:12px; padding:1.2rem; margin:2rem 0; background:#f5faf9; }
.memory-card h3,.memory-card h4 { color:#16585f; }
.memory-flow { display:flex; gap:.6rem; align-items:stretch; margin:1rem 0; flex-wrap:wrap; }
.memory-node { flex:1 1 12rem; background:#16585f; color:white; border-radius:8px; padding:.8rem; }
.memory-node b { display:block; font-size:1.4rem; opacity:.7; }
.memory-arrow { align-self:center; color:#216870; font-size:1.5rem; }
.memory-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,22rem),1fr)); gap:1rem; }
.memory-section { background:white; border:1px solid #b9d5d3; border-radius:8px; padding:.8rem; min-width:0; }
.memory-section-link { background:white; border:1px solid #b9d5d3; border-radius:8px; padding:.8rem; }
.section-memory-card { margin:1.2rem 0; border:2px solid #216870; padding:1rem; background:#f5faf9; }
.section-memory-card .memory-node { flex-basis:14rem; font-size:.9rem; }
.section-memory-card .memory-node b { font-size:1rem; opacity:1; margin-bottom:.4rem; }
.section-memory-formulas { overflow-x:auto; }.section-memory-formulas h5 { font-size:1rem; margin:.7rem 0; }
.section-memory-formulas li { padding:.3rem 0; }.section-memory-table { overflow-x:auto; margin:.7rem 0; }
.section-memory-card summary { cursor:pointer; color:#16585f; }
.memory-section h4 { margin-top:0; }.memory-section .memory-formulas { overflow-wrap:anywhere; }
.memory-rule { background:#e7f1ef; border-left:4px solid #247f77; padding:.5rem .8rem; margin:.5rem 0; }
.memory-section details { margin-top:.6rem; }.memory-section summary { cursor:pointer; color:#16585f; }
.memory-answer { border-top:1px solid #d5e1de; padding:.6rem 0; scroll-margin-top:1rem; }
.memory-answer p { margin:.35rem 0; }.memory-answer .memory-explanation { font-size:.9rem; }
.memory-answer:target { outline:2px solid #247f77; outline-offset:4px; }
.lesson-vocab small { display:block; color:#536e87; font-size:.8rem; }.lesson-vocab .vocab-help { font-weight:normal; font-size:.85rem; }
.glossary-nav { display:flex; flex-wrap:wrap; gap:.6rem; position:relative; }
.radio-glossary table { width:100%; table-layout:fixed; }.radio-glossary td { overflow-wrap:anywhere; }
.radio-glossary th:first-child { width:26%; }.radio-glossary small { display:block; color:#536e87; }
@media print { .memory-card,.memory-section { break-inside:avoid; }.memory-node { color:#111; background:#e7f1ef; } }
</style>'''


def section_memory_card(unit, document):
    """Keep each lesson's mnemonic and question evidence beside that lesson."""
    sid = unit['id']
    guide = data('study_guide.json')['sections'][sid]
    heading = re.search(r'<h3 id="'+re.escape(sid)+r'"[^>]*>(.*?)</h3>', document, re.S)
    title = re.sub(r'<span\b.*', '', heading[1], flags=re.S).strip()
    body = re.search(r'<div class="lesson-body" data-section="'+sid+r'">(.*?)</div>\s*<aside class="section-summary"',document,re.S)
    body_html = body[1] if body else ''
    formulas = list(dict.fromkeys(re.findall(r'\\\(.*?\\\)|\\\[.*?\\\]', body_html, re.S)))
    def symbolic_formula(formula):
        # Single symbols and worked-example substitutions are not standalone recall rules.
        parts = formula.split('=')
        if len(parts) < 2:
            return False
        for right in parts[1:]:
            right = re.sub(r'\\(?:text|mathrm)\{[^}]*\}', '', right)
            right = re.sub(r'\\[A-Za-z]+', '', right)
            if not re.search(r'[A-Za-z]', right):
                return False
        return True
    formulas = [formula for formula in formulas if symbolic_formula(formula)]
    questions = section_questions(unit['anchors'])
    cards = card_content()
    reviews = []
    for q in questions:
        number = str(q['num']); c = cards[number]
        explanation = re.split(r'<div class="sec">重点词汇</div>', c['原理讲解'])[0]
        reviews.append(f'<article class="memory-answer" id="review-{sid}-{number}" data-question="{number}">'
                       f'<p><b>题 {number}</b> · <span lang="fr">{text_html(q["question"])}</span></p>'
                       f'<p>{c["题干中译"]}</p><p><b>答案 {chr(65+q["reponse"])}</b>：'
                       f'<span lang="fr">{text_html(q["propositions"][q["reponse"]])}</span></p>'
                       f'<div class="memory-explanation">{explanation or c["注释中译"] or esc(guide["summary"])}</div>'
                       f'<a href="#{sid}">返回本节完整习题与题图</a></article>')
    from study_polish import NOTES
    warnings = ''.join('<p class="memory-rule">'+esc(w)+'</p>' for w in NOTES.get(sid,[]) if w)
    concepts = ' · '.join(guide['keywords'])
    check = '核对题目条件、单位与选项；计算题将结果代回原式，识图题对照原题图。' if questions else '对照正文掌握概念；本节暂无直接关联题。'
    steps = [('读题：辨认概念', concepts), ('推理：抓住关系', guide['summary']), ('作答：复核条件', check)]
    flow = '<span class="memory-arrow" aria-hidden="true">→</span>'.join(
        '<div class="memory-node"><b>'+esc(label)+'</b>'+esc(text)+'</div>' for label,text in steps)
    formula_list = lambda values: '<ul>'+''.join('<li>'+formula+'</li>' for formula in values)+'</ul>'
    extra_formulas = ('<details><summary>其余公式与变形</summary>'+formula_list(formulas[8:])+'</details>') if len(formulas)>8 else ''
    formula_block = ('<div class="section-memory-formulas"><h5>公式与变形速查</h5>'
                     + formula_list(formulas[:8])+extra_formulas+'</div>') if formulas else ''
    # Reuse the edited lesson's comparison tables rather than retyping regulatory values or codes.
    from bs4 import BeautifulSoup
    tables = BeautifulSoup(body_html, 'html.parser').find_all('table')
    table_blocks = []
    for table in tables:
        if table.find_parent('table'):
            continue
        for node in [table, *table.find_all(True)]:
            node.attrs.pop('id', None)
        table_blocks.append('<div class="section-memory-table">'+str(table)+'</div>')
    references = ('<details class="section-memory-reference"><summary>本节对照表（展开速查）</summary>'
                  + ''.join(table_blocks)+'</details>') if table_blocks else ''
    review = (f'<details class="memory-review"><summary>题型与解题依据：逐题核对 {len(questions)} 道</summary>'
              + ''.join(reviews)+'</details>') if questions else ''
    return (f'<section class="memory-section section-memory-card" id="memory-section-{sid}" data-section="{sid}" aria-label="本节知识速记卡">'
            f'<h4>本节知识速记卡 · <a href="#{sid}">{title}</a></h4>'
            '<div class="memory-flow">'+flow+'</div>'+formula_block+warnings+references+review+'</section>')


def chapter_section_link(unit, document):
    sid = unit['id']
    heading = re.search(r'<h3 id="'+re.escape(sid)+r'"[^>]*>(.*?)</h3>', document, re.S)
    title = re.sub(r'<span\b.*', '', heading[1], flags=re.S).strip()
    summary = data('study_guide.json')['sections'][sid]['summary']
    return (f'<section class="memory-section-link"><h4><a href="#memory-section-{sid}">{title} · 小节速记卡 →</a></h4>'
            '<p>'+esc(summary)+'</p></section>')


def memory_card(cid, units, document):
    chapter = data('chapter_memory.json')[cid]
    steps = '<span class="memory-arrow" aria-hidden="true">→</span>'.join(
        f'<div class="memory-node"><b>{i}</b>{esc(s)}</div>' for i,s in enumerate(chapter['steps'],1))
    rules = ''.join(f'<p class="memory-rule">{esc(s)}</p>' for s in chapter['rules'])
    panels = ''.join(chapter_section_link(unit,document) for unit in units)
    return (f'<section class="memory-card" id="memory-{cid}" data-chapter="{cid}" aria-label="本章知识速记卡">'
            f'<h3>本章知识速记卡 · {cid}</h3><p>按流程图复习全章；每节正文之后另有独立速记卡，含公式、对照表与逐题解题依据。</p>'
            '<div class="memory-flow">'+steps+'</div>'+rules+'<div class="memory-grid">'+panels+'</div></section>')


def add_section_memory_cards(document, units):
    if 'class="memory-section section-memory-card"' in document:
        raise ValueError('Section memory cards already present')
    by_id = {u['id']:u for u in units}
    seen = set()
    def insert(match):
        sid = match[1]
        if sid in seen or sid not in by_id:
            raise ValueError(f'Duplicate or unknown lesson: {sid}')
        seen.add(sid)
        return match[0] + '\n' + section_memory_card(by_id[sid],document) + '\n'
    document = re.sub(r'<aside class="lesson-vocab" data-section="([^"]+)".*?</aside>',insert,document,flags=re.S)
    if seen != set(by_id):
        raise ValueError('Some lessons have no memory card')
    return document


def glossary_html():
    entries = data('alphabetical_vocab.json')
    grouped = {}
    for e in entries:
        letter = key(e['fr'])[0].upper()
        if not ('A' <= letter <= 'Z'): letter = '#'
        grouped.setdefault(letter,[]).append(e)
    out = ['<section class="radio-glossary" id="radio-glossary"><h2>附录 H　无线电法语词汇表（按首字母排序）</h2>',
           '<p>法语字母排序，重音符号按基础字母处理；含题目中常见的进阶动词及其变位。例句直接取自题干或选项。已有词表中未在题干／选项直接出现的词，标作补充术语。</p>',
           '<nav class="glossary-nav" aria-label="词汇首字母导航">'+''.join(f'<a href="#glossary-{a}">{a}</a>' for a in grouped)+'</nav>']
    from gen_common import load_questions
    bank = {str(q['num']):q for q in load_questions()['questions']}
    for letter, rows in grouped.items():
        out.append(f'<h3 id="glossary-{letter}">{letter}</h3><table><thead><tr><th>法语／词性</th><th>中文、用法与题目语境</th></tr></thead><tbody>')
        for e in rows:
            refs = e['questions']
            note = '<small>'+esc(e['note'])+'</small>' if e['note'] else ''
            example = ''
            if refs:
                q = bank[refs[0]]
                phrases = [q['question']] + q['propositions']
                from build_learning_vocab import occurs
                example_text = next((p for p in phrases if occurs(e['fr'], p)), q['question'])
                # Infinitives can be absent from the actual sentence; prefer a recorded inflected form.
                if e['note'].startswith('题中形式：'):
                    forms = e['note'][5:].split('、')
                    example_text = next((p for p in phrases if any(occurs(f,p) for f in forms)),example_text)
                example = f'<small>题 {refs[0]} · <span lang="fr">{text_html(example_text)}</span></small>'
            else: example = '<small>补充术语（已有词表）</small>'
            out.append(f'<tr class="glossary-entry"><td><span lang="fr">{esc(e["fr"])}</span><small>{esc(e["category"])}</small></td><td>{esc(e["zh"])}{note}{example}</td></tr>')
        out.append('</tbody></table>')
    return ''.join(out)+'</section>'


def add_learning_supplements(document, units):
    if 'id="learning-supplement-style"' in document:
        raise ValueError('Learning supplements already present')
    document = re.sub(r'<aside class="lesson-vocab" data-section="([^"]+)".*?</aside>',
                      lambda m: expanded_vocabulary(m[1]), document, flags=re.S)
    document = add_section_memory_cards(document, units)
    groups = {}
    for u in units:
        sid = u['id']; cid = 'R-'+sid[1] if sid.startswith('R') else 'T-'+str(int(sid[1:3]))
        groups.setdefault(cid,[]).append(u)
    # Insert before the following chapter heading, keeping the existing lesson HTML intact.
    for cid, chapter_units in reversed(list(groups.items())):
        start = document.index('<h2 id="chap-'+cid+'"')
        following = re.search(r'<h2\b',document[start+4:])
        end = start+4+following.start() if following else document.index('</main>')
        document = document[:end]+memory_card(cid,chapter_units,document)+document[end:]
    document = re.sub(r'(<aside class="chapter-summary" data-chapter="([^"]+)".*?</aside>)',
                      lambda m: m[1] + '<p class="memory-jump"><a href="#memory-' + m[2] + '">跳到本章知识速记卡 →</a></p>',
                      document, flags=re.S)
    document = document.replace('</main>',glossary_html()+'</main>',1)
    document = document.replace('<li><a href="#annexes">附录</a>', '<li><a href="#radio-glossary">A–Z 无线电法语词汇表</a></li><li><a href="#annexes">附录</a>',1)
    document = document.replace('</head>',CSS+'</head>',1)
    # Reveal a linked review entry even if its enclosing details is collapsed.
    script = '''<script id="learning-links-script">(function(){function reveal(){var id;try{id=decodeURIComponent(location.hash.slice(1));}catch(e){return;}var target=document.getElementById(id);if(!target)return;for(var p=target.parentElement;p;p=p.parentElement){if(p.tagName==='DETAILS')p.open=true;}requestAnimationFrame(function(){target.scrollIntoView({block:'start'});});}window.addEventListener('hashchange',reveal);if(location.hash)reveal();})();</script>'''
    return document.replace('</body>',script+'</body>',1)
