#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Verification finale des trois livrables + rapport de synthese.
import collections, csv, html.parser, json, os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE, '..'))
sys.path.insert(0, BASE)
from gen_common import questions_by_anchor, load_questions      # noqa: E402


class Checker(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.stack, self.errors = [], [], [], []
        self.void = {'br', 'img', 'meta', 'link', 'hr', 'input'}
        self.auto = {'li', 'p', 'td', 'th', 'tr', 'option'}

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if 'id' in d:
            self.ids.append(d['id'])
        if tag == 'a' and d.get('href', '').startswith('#'):
            self.links.append(d['href'][1:])
        if tag not in self.void:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.void:
            return
        while self.stack:
            top = self.stack.pop()
            if top == tag:
                return
            if top not in self.auto:
                self.errors.append('</%s> ferme <%s>' % (tag, top))
                return
        self.errors.append('</%s> sans ouverture' % tag)


def size(p):
    return '%.1f KB' % (os.path.getsize(p) / 1024.0) if os.path.exists(p) else 'ABSENT'


def main():
    print('=' * 72)
    print('1. FICHIERS')
    for f in ('manuel-zh.html', 'vocabulaire.csv', 'README.md'):
        print('   %-20s %s' % (f, size(os.path.join(ROOT, f))))

    # ---------------------------------------------------------- HTML
    hp = os.path.join(ROOT, 'manuel-zh.html')
    doc = open(hp, encoding='utf-8').read()
    c = Checker()
    c.feed(doc)
    dups = [k for k, v in collections.Counter(c.ids).items() if v > 1]
    broken = sorted({l for l in c.links if l not in set(c.ids)})
    print('\n2. HTML')
    print('   taille            : %s' % size(hp))
    print('   parse html.parser : OK')
    print('   ancres id         : %d (doublons : %s)' % (len(c.ids), dups or 'aucun'))
    print('   liens internes    : %d, casses : %s' % (len(set(c.links)), broken or 'aucun'))
    print('   erreurs imbrication : %s' % (c.errors[:6] or 'aucune'))
    print('   balises interdites  : %s'
          % (sorted({t for t in re.findall(r'<(script|style|iframe|img|link)\b', doc, re.I)})
             or 'aucune'))
    print('   ressources externes : %s'
          % (re.findall(r'(?:src|href)="(https?://[^"]+)"', doc)[:3] or 'aucune'))

    # ---------------------------------------------------------- sections
    plan = json.load(open(os.path.join(BASE, 'plan.json'), encoding='utf-8'))
    units = plan['units']
    idx = questions_by_anchor()
    printed = re.findall(r'<h3 id="([^"]+)"', doc)
    print('\n3. MANUEL')
    print('   sections (unites du plan) : %d' % len(units))
    print('   sections rendues          : %d' % len(printed))
    print('   signets distincts couverts: %d / %d'
          % (len({a for u in units for a in (u.get("anchors") or [u["id"]])}),
             len([a for a in idx if a])))
    print('   questions rattachees      : %d / %d'
          % (sum(u['nq'] for u in units), len(load_questions()['questions'])))
    print('   encadres 高频考点         : %d' % doc.count('class="exam"'))
    print('   questions traduites       : %d' % doc.count('<details><summary>'))
    print('   avertissements 待核实      : %d' % doc.count('class="warn"'))
    chaps = collections.Counter()
    for u in units:
        s = u['section']
        chaps['R-' + s[1] if s[0] == 'R' else 'T-' + str(int(s[1:3]))] += 1
    print('   chapitres                 : %d' % len(chaps))
    vig = sorted(units, key=lambda u: -u['nq'])[:10]
    print('   top 10 par题量            : '
          + ', '.join('%s(%d)' % (u['id'], u['nq']) for u in vig))

    # ---------------------------------------------------------- CSV
    vp = os.path.join(ROOT, 'vocabulaire.csv')
    print('\n4. VOCABULAIRE')
    if os.path.exists(vp):
        with open(vp, encoding='utf-8', newline='') as f:
            rows = list(csv.reader(f))
        head, body = rows[0], rows[1:]
        print('   entetes   : %s' % head)
        print('   lignes    : %d' % len(body))
        print('   taille    : %s' % size(vp))
        print('   categories: %s' % dict(collections.Counter(r[2] for r in body).most_common()))
        print('   themes    : %d distincts' % len({r[4] for r in body}))
        bad = [r for r in body if len(r) != 6 or not r[0] or not r[1]]
        print('   lignes malformees : %d' % len(bad))
        print('   sans 备注 : %d' % sum(1 for r in body if not r[5]))
        print('   exemple   : %s' % body[0])
    else:
        print('   ABSENT')

    # ---------------------------------------------------------- avertissements
    warns = re.findall(r'<div class="warn">(.*?)</div>', doc, re.S)
    print('\n5. POINTS A VERIFIER (%d)' % len(warns))
    for w in warns[:60]:
        t = re.sub(r'<[^>]+>', '', w)
        t = re.sub(r'\s+', ' ', t).strip()
        print('   -', t[:150])
    print('=' * 72)


if __name__ == '__main__':
    main()
