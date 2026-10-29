import json, re, glob

BASE = '/home/thelia/Documents/radioamateur-fr/source/full/'

def cn_len(s):
    return len(re.findall(r'[\u4e00-\u9fff]', s))

src = json.load(open(BASE + 'slice_4.json'))
srcm = {x['num']: x for x in src}
order = [x['num'] for x in src]

out = {}
problems = []
for p in sorted(glob.glob(BASE + 'out_4_p*.json')):
    d = json.load(open(p))
    dup = [k for k in d if k in out]
    if dup: problems.append('%s 与其他片重复: %s' % (p, dup))
    out.update(d)

missing = [n for n in order if n not in out]
extra = [k for k in out if k not in srcm]
if missing: problems.append('缺失 %d 条: %s' % (len(missing), missing[:20]))
if extra: problems.append('多余 %d 条: %s' % (len(extra), extra[:20]))

for n, e in out.items():
    for k in ('stem_zh','ans_zh','com_zh','explain'):
        if k not in e or not isinstance(e[k], str):
            problems.append('%s 字段 %s 问题' % (n, k))
    s = e.get('explain','')
    L = cn_len(s)
    if L < 80 or L > 250: problems.append('%s explain 字数 %d' % (n, L))
    if '$' in s: problems.append('%s explain 含 $' % n)
    if srcm.get(n,{}).get('commentaire_fr','') == '' and e.get('com_zh','') != '':
        problems.append('%s com_zh 应为空' % n)
    if srcm.get(n,{}).get('commentaire_fr','') != '' and e.get('com_zh','') == '':
        problems.append('%s com_zh 不该为空' % n)

ordered = {n: out[n] for n in order if n in out}
json.dump(ordered, open(BASE + 'out_4.json','w'), ensure_ascii=False, indent=1)

print('合并条数:', len(ordered), '/', len(order))
print('待核条数:', sum(1 for e in ordered.values() if '⚠️待核' in e['stem_zh'] or '⚠️待核' in e['ans_zh'] or '⚠️待核' in e['com_zh']))
print('问题数:', len(problems))
for x in problems[:50]: print(' -', x)
