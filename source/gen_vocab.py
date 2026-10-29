#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Fusionne les trois lots de glossaires et ecrit ../vocabulaire.csv
# (6 colonnes, trie par frequence decroissante).
import csv, os, sys, re, collections, importlib

BASE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(BASE, 'work')
DEST = os.path.abspath(os.path.join(BASE, '..', 'data', 'vocabulaire.csv'))
HEAD = ['Français', '中文', '词性/类别', '频次', '所属主题', '备注']


def main():
    rows, seen = [], set()
    for tag in ('part1', 'part2', 'part3', 'extra'):
        p = os.path.join(WORK, 'vocab_%s.csv' % tag)
        if not os.path.exists(p):
            print('!! lot manquant :', p)
            continue
        with open(p, encoding='utf-8', newline='') as f:
            n = 0
            for r in csv.reader(f):
                if not r or len(r) < 5:
                    continue
                r = (r + ['', '', '', '', '', ''])[:6]
                fr = r[0].strip()
                if not fr:
                    continue
                low = re.sub(r'\s+', ' ', fr.lower())
                if low in seen:
                    continue
                seen.add(low)
                try:
                    freq = int(r[3])
                except ValueError:
                    freq = 0
                rows.append([fr, r[1].strip(), r[2].strip(), freq, r[4].strip(), r[5].strip()])
                n += 1
            print('lot %s : %d lignes' % (tag, n))
    # fusion des doublons de casse/accents (garde la frequence maximale)
    merged = {}
    for r in rows:
        key = re.sub(r'\s+', ' ', r[0].lower())
        if key in merged and merged[key][3] >= r[3]:
            continue
        merged[key] = r
    rows = sorted(merged.values(), key=lambda r: (-r[3], r[0].lower()))
    with open(DEST, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(HEAD)
        w.writerows(rows)
    cats = collections.Counter(r[2] for r in rows)
    the = collections.Counter(r[4] for r in rows)
    print('-> %s : %d entrees (%.1f Ko)'
          % (DEST, len(rows), os.path.getsize(DEST) / 1024.0))
    print('categories :', dict(cats.most_common()))
    print('themes :', dict(the.most_common()))


if __name__ == '__main__':
    main()
