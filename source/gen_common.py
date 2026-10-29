#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Outils communs pour la generation du manuel chinois de preparation au
# certificat d'operateur du service amateur (F6KGL, CC BY-NC-SA 4.0).
# - chargement des 2692 questions (Exam1)
# - analyse des identifiants de signets (#R21b, #T023g2 ...)
# - nettoyage du texte brut de cours.txt (issu d'une conversion PDF)
import json, os, re, html

BASE = os.path.dirname(os.path.abspath(__file__))
QUESTIONS = os.path.join(BASE, 'Exam1', 'questions', 'questions.json')
COURS = os.path.join(BASE, 'cours.txt')

_q = None


def load_questions():
    global _q
    if _q is None:
        _q = json.load(open(QUESTIONS, encoding='utf-8'))
    return _q


def theme_names():
    return {t['num']: t['nom'] for t in load_questions()['themes']}


def anchor_of(q):
    # Renvoie l'identifiant de signet (ex. 'R21b') ou ''.
    c = q.get('cours') or ''
    if '#' not in c:
        return ''
    return c.split('#')[-1].strip().rstrip('.')


RE_R = re.compile(r'^R(\d)(\d+)([a-z]\d*)?$')
RE_T = re.compile(r'^T(\d\d)(\d+)([a-z]\d*)?$')


def parse_anchor(a):
    # Decoupe un signet en (partie, chapitre, paragraphe, signet).
    m = RE_R.match(a)
    if m:
        ch, sec = int(m.group(1)), int(m.group(2))
        return {'part': 'R', 'chapter': ch, 'section': sec,
                'signet': m.group(3) or '', 'ref': 'R-%d.%d' % (ch, sec)}
    m = RE_T.match(a)
    if m:
        ch, sec = int(m.group(1)), int(m.group(2))
        return {'part': 'T', 'chapter': ch, 'section': sec,
                'signet': m.group(3) or '', 'ref': '%d.%d' % (ch, sec)}
    return None


def norm_anchor(a):
    a = (a or '').strip().rstrip('.')
    a = re.sub(r'\)+$', '', a)
    a = a.replace('T023ac8', 'T023c8')
    m = RE_R.match(a)
    if m:
        return 'R%d%d%s' % (int(m.group(1)), int(m.group(2)), m.group(3) or '')
    m = RE_T.match(a)
    if m:
        return 'T%02d%d%s' % (int(m.group(1)), int(m.group(2)), m.group(3) or '')
    return a


def section_code(a):
    # Code de section (chapitre+paragraphe) : R21b -> R21, T023g2 -> T023.
    p = parse_anchor(a)
    if not p:
        return None
    if p['part'] == 'R':
        return 'R%d%d' % (p['chapter'], p['section'])
    return 'T%02d%d' % (p['chapter'], p['section'])


def questions_by_anchor():
    d = {}
    for q in load_questions()['questions']:
        d.setdefault(norm_anchor(anchor_of(q)), []).append(q)
    return d


def section_questions(anchors):
    # Questions rattachees a une liste de signets.
    idx = questions_by_anchor()
    out = []
    for a in anchors:
        out.extend(idx.get(norm_anchor(a), []))
    out.sort(key=lambda q: q['num'])
    return out


def count_section(anchors):
    return len(section_questions(anchors))


def pick_questions(anchors, n=4):
    # Choisit n questions reparties sur les signets donnes (deterministe).
    idx = questions_by_anchor()
    pools = []
    for a in anchors:
        pool = sorted(idx.get(norm_anchor(a), []), key=lambda q: q['num'])
        if pool:
            pools.append(pool)
    if not pools:
        return []
    pools.sort(key=len, reverse=True)
    picked, seen = [], set()
    rnd = 0
    while len(picked) < n and rnd < 8:
        for pool in pools:
            if len(picked) >= n:
                break
            k = len(pool)
            step = max(1, k // max(1, n))
            pos = (rnd * step) % k
            for offset in range(k):
                q = pool[(pos + offset) % k]
                if q['num'] not in seen:
                    seen.add(q['num'])
                    picked.append(q)
                    break
        rnd += 1
    picked.sort(key=lambda q: q['num'])
    return picked[:n]


# ------------------------------------------------------------------ cours.txt
HEAD = re.compile(r'((?:R-)?\d+\.\d+)\)')


def _is_heading(s):
    if '....' in s:
        return False
    m = HEAD.search(s)
    if not m or s.index(m.group(1)) > 4:
        return False
    return len(s) < 95


def clean_cours():
    # Liste [(no_ligne, texte)] : paragraphes nettoyes, titres prefixes de '###'.
    raw = open(COURS, encoding='utf-8', errors='replace').read()
    raw = raw.replace('\xad', '').replace('\u00a0', ' ')
    lines = raw.split('\n')
    out, buf, start = [], [], 0

    def flush(no):
        if not buf:
            return
        p = re.sub(r'\s+', ' ', ' '.join(buf)).strip()
        p = re.sub(r'\s+([,;:.!?])', r'\1', p)
        if p:
            out.append((no, p))
        buf.clear()

    for i, l in enumerate(lines):
        s = l.strip()
        if _is_heading(s):
            flush(start)
            out.append((i + 1, '### ' + s))
            continue
        if not s or re.fullmatch(r'[-–—o·•]+', s):
            flush(start)
            continue
        if not buf:
            start = i + 1
        buf.append(s)
    flush(start)
    return out


def cours_blocks():
    # Paragraphes nettoyes regroupes par titre de section.
    blocks, cur = [], None
    for no, p in clean_cours():
        if p.startswith('### '):
            cur = {'line': no, 'title': p[4:].strip(), 'paras': []}
            blocks.append(cur)
        else:
            if cur is None:
                cur = {'line': no, 'title': '(introduction)', 'paras': []}
                blocks.append(cur)
            cur['paras'].append(p)
    return blocks


def esc(s):
    return html.escape(s, quote=False)


if __name__ == '__main__':
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'stats'
    if cmd == 'stats':
        qs = load_questions()['questions']
        idx = questions_by_anchor()
        print('questions:', len(qs), '| signets distincts:', len(idx))
        print('sections:', len({section_code(a) for a in idx if section_code(a)}))
    elif cmd == 'blocks':
        for b in cours_blocks():
            print(b['line'], b['title'][:90])
    elif cmd == 'dump':
        for no, p in clean_cours():
            print('%d\t%s' % (no, p))
