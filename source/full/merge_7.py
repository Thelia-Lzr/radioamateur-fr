import json, re, sys

out = {}
order = []
for k in range(1, 6):
    part = json.load(open(f'o7_{k}.json'))
    for n, v in part.items():
        if n in out:
            print('DUPLICATE', n)
        out[n] = v
src = json.load(open('slice_7.json'))
order = [x['num'] for x in src]
missing = [n for n in order if n not in out]
extra = [n for n in out if n not in order]
print('src', len(order), 'out', len(out), 'missing', missing, 'extra', extra)

# field + format checks
bad = 0
for x in src:
    n = x['num']
    if n not in out: continue
    o = out[n]
    for f in ('stem_zh', 'ans_zh', 'com_zh', 'explain'):
        if f not in o or not isinstance(o[f], str):
            print(n, 'BADFIELD', f); bad += 1
    e = o.get('explain', '')
    L = len(re.findall(r'[\u4e00-\u9fff]', e))
    if not (80 <= L <= 250):
        print(n, 'LEN', L); bad += 1
    blob = json.dumps(o, ensure_ascii=False)
    if '$' in blob:
        print(n, 'DOLLAR'); bad += 1
    for m in re.findall(r'\d,\d+', blob):
        print(n, 'COMMA-NUM', m)
print('bad', bad)

if not missing and not extra:
    merged = {n: out[n] for n in order}
    json.dump(merged, open('out_7.json', 'w'), ensure_ascii=False, indent=1)
    print('WROTE out_7.json', len(merged))
