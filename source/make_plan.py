#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Construit le plan du manuel : unites de redaction (une par section du cours,
# subdivisee par signet quand la section est tres fournie) + affectation en
# blocs de redaction + selection deterministe des questions d'examen.
import json, os, collections, re as _re
from gen_common import (questions_by_anchor, section_code, parse_anchor,
                        norm_anchor, cours_blocks, pick_questions, count_section)
import re

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, 'plan.json')

# blocs de redaction : (nom, ligne_debut, ligne_fin)
BLOCKS = [
    ('W1', 852, 1741),
    ('W2', 1741, 2657),
    ('W3', 2657, 3380),
    ('W4', 3380, 3813),
    ('W4b', 3813, 4478),
    ('W5', 4478, 5960),
    ('W6', 5960, 7211),
    ('W7', 7211, 8392),
    ('W8', 8392, 9256),
    ('W9', 9256, 10102),
    ('W10', 10102, 10700),
    ('W11', 10700, 11436),
]

SPLIT_AT = 60   # au dela, la section est decoupee par signet
MINI = 10       # un signet avec au moins MINI questions devient une unite a part

# signets mal formes dans la base de questions -> section la plus proche
FIX = {'R013b': 'R13', 'T0112a': 'T112', 'T07': 'T071', 'T11': 'T111',
       'T03e': 'T033', 'T023ac8': 'T023', 'T107a': 'T017'}


def sec_of_heading(txt):
    # titre de la forme 'R-1.2) ...' ou 'a 9.10) ...' -> ('R'|'T', ch, sec)
    m = re.search(r'(R-)?(\d+)\.(\d+)\)', txt)
    if not m:
        return None
    return ('R' if m.group(1) else 'T', int(m.group(2)), int(m.group(3)))


def code_of(part, ch, sec):
    return ('R%d%d' % (ch, sec)) if part == 'R' else ('T%02d%d' % (ch, sec))


def main():
    idx = questions_by_anchor()
    blocks_cours = [b for b in cours_blocks() if b['line'] > 840]
    # titre francais et position de chaque section
    sec_title, sec_line = {}, {}
    for b in blocks_cours:
        p = sec_of_heading(b['title'])
        if not p:
            continue
        code = code_of(*p)
        if code not in sec_line:
            sec_line[code] = b['line']
            sec_title[code] = b['title'].split(')', 1)[-1].strip() or b['title']

    bysect = collections.defaultdict(list)
    for a, qs in idx.items():
        sc = section_code(a)
        if not a or not qs:
            continue
        if a in FIX:
            sc = FIX[a]
        if sc:
            bysect[sc].append(a)
    # un signet mal forme change de section : on evite les doublons
    for sc, anchors in bysect.items():
        seen, uniq = set(), []
        for a in anchors:
            if a not in seen:
                seen.add(a)
                uniq.append(a)
        bysect[sc] = uniq
    # emplacement fallback des sections sans titre reperé
    def line_of(code):
        if code in sec_line:
            return sec_line[code]
        part = code[0]
        ch = int(code[1]) if part == 'R' else int(code[1:3])
        sec = int(code[2:]) if part == 'R' else int(code[3:])
        same = []
        for k, v in sec_line.items():
            if k[0] != part:
                continue
            kch = int(k[1]) if part == 'R' else int(k[1:3])
            ksec = int(k[2:]) if part == 'R' else int(k[3:])
            if kch == ch:
                same.append((ksec, v))
        if same:
            same.sort()
            prev = [v for s, v in same if s < sec]
            if prev:
                return max(prev)
            return same[0][1]
        return 0

    units = []
    for code, anchors in bysect.items():
        total = sum(len(idx[a]) for a in anchors)
        if total >= SPLIT_AT:
            # signets fournis -> unites autonomes ; le reste -> unite generale
            big = [a for a in anchors if len(idx[a]) >= MINI and a != code]
            rest = [a for a in anchors if a not in big]
            big.sort(key=lambda a: -len(idx[a]))
            for a in big:
                p = parse_anchor(a)
                units.append({
                    'id': a, 'section': code, 'anchors': [a],
                    'ref': '%s.%s' % (p['ref'], p['signet']),
                    'nq': len(idx[a]), 'title_fr': sec_title.get(code, ''),
                    'line': line_of(code), 'main': False})
            if rest:
                p = parse_anchor(code)
                units.append({
                    'id': code, 'section': code, 'anchors': sorted(rest),
                    'ref': p['ref'] if p else code,
                    'nq': sum(len(idx[a]) for a in rest),
                    'title_fr': sec_title.get(code, ''),
                    'line': line_of(code), 'main': True})
        else:
            p = parse_anchor(code)
            units.append({
                'id': code, 'section': code, 'anchors': sorted(anchors),
                'ref': p['ref'] if p else code,
                'nq': total, 'title_fr': sec_title.get(code, ''),
                'line': line_of(code), 'main': True})

    # identifiants uniques
    # sections du cours sans aucune question : unites breves de completude
    have = {u['section'] for u in units}
    for code in sec_line:
        if code in have or not _re.match(r'^[RT]\d+$', code):
            continue
        p = parse_anchor(code)
        units.append({
            'id': code, 'section': code, 'anchors': [],
            'ref': p['ref'] if p else code,
            'nq': 0, 'title_fr': sec_title.get(code, ''),
            'line': line_of(code), 'main': True})
    used = collections.Counter()
    for u in units:
        used[u['id']] += 1
    for u in units:
        if used[u['id']] > 1:
            u['id'] = u['id'] + '_' + (u['ref'].replace('.', '') or 'x')
    ids = {u['id'] for u in units}
    assert len(ids) == len(units), 'identifiants non uniques'

    units.sort(key=lambda u: (u['line'], 0 if u['main'] else 1, -u['nq']))

    # affectation aux blocs
    for u in units:
        u['block'] = None
        for name, lo, hi in BLOCKS:
            if lo <= u['line'] < hi:
                u['block'] = name
                break
        if u['block'] is None:
            u['block'] = 'W1' if u['line'] < 852 else 'W11'

    # questions exemplaires
    for u in units:
        n = 4 if u['nq'] >= 8 else max(1, u['nq'])
        u['picks'] = pick_questions(u['anchors'], n)

    plan = {'units': units,
            'blocks': {name: {'lo': lo, 'hi': hi,
                              'units': [u['id'] for u in units if u['block'] == name]}
                       for name, lo, hi in BLOCKS}}
    json.dump(plan, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    # fichiers de travail par bloc (questions a traduire)
    wk = os.path.join(BASE, 'work')
    os.makedirs(wk, exist_ok=True)
    # texte nettoye du cours, decoupe par bloc
    clean = [(no, p) for no, p in __import__('gen_common').clean_cours()]
    for name, lo, hi in BLOCKS:
        us = [u for u in units if u['block'] == name]
        data = []
        for u in us:
            depth = 1 if u['nq'] >= 20 else (2 if u['nq'] >= 8 else 3)
            data.append({'id': u['id'], 'ref': u['ref'], 'nq': u['nq'],
                         'depth': depth, 'anchors': u['anchors'],
                         'title_fr': u['title_fr'],
                         'questions': [{'num': q['num'], 'question': q['question'],
                                        'reponse': q['propositions'][q['reponse']]}
                                       for q in u['picks']]})
        json.dump({'block': name, 'lines': [lo, hi], 'units': data},
                  open(os.path.join(wk, 'block_%s.json' % name), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        with open(os.path.join(wk, 'cours_%s.txt' % name), 'w', encoding='utf-8') as f:
            for no, p in clean:
                if lo <= no < hi:
                    f.write(p + '\n')
    print('unites:', len(units), '| blocs:', len(BLOCKS))
    for name, lo, hi in BLOCKS:
        us = [u for u in units if u['block'] == name]
        print('%s lignes %d-%d : %d unites, %d questions'
              % (name, lo, hi, len(us), sum(u['nq'] for u in us)))


if __name__ == '__main__':
    main()
