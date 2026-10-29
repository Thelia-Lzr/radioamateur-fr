# -*- coding: utf-8 -*-
import json, sys, os, re, importlib.util

base = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(base, 'out_3.json')
out = {}
if os.path.exists(out_path):
    out = json.load(open(out_path, encoding='utf-8'))

for name in sys.argv[1:]:
    spec = importlib.util.spec_from_file_location(name, os.path.join(base, name + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for k, v in mod.DATA.items():
        assert isinstance(v, str) and v.strip(), k
        out[k] = v

json.dump(out, open(out_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

src = json.load(open(os.path.join(base, 'slice_3.json'), encoding='utf-8'))
nums = [x['num'] for x in src]
missing = [n for n in nums if n not in out]
extra = [n for n in out if n not in set(nums)]
print('keys in out_3.json :', len(out), '/ 227')
print('missing            :', len(missing), missing[:30])
print('extra              :', extra)

def cjk(s):
    return len(re.findall(r'[\u4e00-\u9fff]', s))

bad = [(k, cjk(v)) for k, v in out.items() if not (80 <= cjk(v) <= 250)]
print('CJK count out of 80-250:', len(bad), bad)
print('json.load check    : OK')
