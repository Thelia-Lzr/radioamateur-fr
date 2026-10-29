#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Controle qualite des modules content_* :
#  - couverture exacte des unites du plan et des numeros de questions
#  - balises interdites
#  - nombres cites qui ne figurent pas dans le texte source du bloc
#    (pour reperer d'eventuelles inventions)
import importlib, json, os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
BLOCKS = ['W1', 'W2', 'W3', 'W4', 'W4b', 'W5', 'W6', 'W7', 'W8', 'W9', 'W10', 'W11']
BAD_TAG = re.compile(r'</?(script|style|html|body|h1|h2|h3|iframe|img|link)\b', re.I)
NUM = re.compile(r'\d+(?:[.,]\d+)?')


def norm(s):
    # rend la comparaison de nombres tolerante aux separateurs
    return re.sub(r'(?<=\d)[.\s](?=\d{3}\b)', '', s)


def main():
    total_warn = 0
    missing_mod = []
    for b in BLOCKS:
        p = os.path.join(BASE, 'content_%s.py' % b)
        if not os.path.exists(p):
            missing_mod.append(b)
            continue
        m = importlib.import_module('content_' + b)
        plan = json.load(open(os.path.join(BASE, 'work', 'block_%s.json' % b), encoding='utf-8'))
        ids = [u['id'] for u in plan['units']]
        got = [s['id'] for s in m.SECTIONS]
        nums = {q['num'] for u in plan['units'] for q in u['questions']}
        miss_q = sorted(nums - set(m.QT))
        allbody = ' '.join(s['body'] for s in m.SECTIONS)
        tags = sorted({t.lower() for t in BAD_TAG.findall(allbody)})
        warns = allbody.count('class="warn"')
        total_warn += warns
        src = open(os.path.join(BASE, 'work', 'cours_%s.txt' % b), encoding='utf-8').read()
        nsrc = norm(src)
        absent = set()
        for n in NUM.findall(allbody):
            if len(n) < 3:
                continue
            if n not in nsrc and n.replace(',', '.') not in nsrc:
                absent.add(n)
        flag = []
        if got != ids:
            flag.append('UNITES!')
        if miss_q:
            flag.append('QT manquants: %s' % ','.join(miss_q[:5]))
        if tags:
            flag.append('TAGS: %s' % tags)
        print('%-4s %2d unites  QT %3d  avert. %2d  nombres hors source %2d  %s'
              % (b, len(m.SECTIONS), len(m.QT), warns, len(absent),
                 ' '.join(flag) or 'OK'))
        if absent:
            print('        hors source :', ', '.join(sorted(absent)[:14]))
    print('---')
    print('modules manquants :', missing_mod or 'aucun')
    print('avertissements (待核实) au total :', total_warn)


if __name__ == '__main__':
    main()
