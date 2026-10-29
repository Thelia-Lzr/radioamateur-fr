"""Merge one batch of knowledge-point cards into out_4.json and validate."""
import json, os, re, sys

P = '/home/thelia/Documents/radioamateur-fr/source/kp/out_4.json'
HAN = re.compile(r'[\u4e00-\u9fff]')


def merge(new, batch_name=''):
    cur = {}
    if os.path.exists(P):
        with open(P, encoding='utf-8') as f:
            cur = json.load(f)
    cur.update(new)
    with open(P, 'w', encoding='utf-8') as f:
        json.dump(cur, f, ensure_ascii=False, indent=1)
    # re-validate from disk
    with open(P, encoding='utf-8') as f:
        d = json.load(f)
    print('=== batch %s written ===' % batch_name)
    print('total keys: %d  ->  %s' % (len(d), ','.join(sorted(d))))
    bad = []
    for k in sorted(d):
        v = d[k]
        nb = len(HAN.findall(v['body']))
        nf = len(HAN.findall(v['front']))
        flag = ''
        if not (400 <= nb <= 800):
            flag = '  <== BODY OUT OF RANGE'
            bad.append(k)
        if len(v['title_zh']) > 12:
            flag += '  <== TITLE TOO LONG(%d)' % len(v['title_zh'])
        if '待核' not in v['body'] and '待核' in v.get('title_zh', ''):
            pass
        print('%s  body=%3d  front=%2d  title_zh=%s%s' % (k, nb, nf, v['title_zh'], flag))
    for k in sorted(d):
        n = d[k]['body'].count('待核')
        if n:
            print('  [待核] %s x%d' % (k, n))
    if bad:
        print('OUT OF RANGE:', bad)
    return d
