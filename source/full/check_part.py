import json, sys, re

def cn_len(s):
    return len(re.findall(r'[\u4e00-\u9fff]', s))

def main():
    path, nums = sys.argv[1], sys.argv[2].split(',')
    nums = [n.strip() for n in nums if n.strip()]
    d = json.load(open(path))
    src = {x['num']: x for x in json.load(open('/home/thelia/Documents/radioamateur-fr/source/full/slice_4.json'))}
    errs = []
    missing = [n for n in nums if n not in d]
    extra = [k for k in d if k not in nums]
    if missing: errs.append('缺少键: %s' % missing)
    if extra: errs.append('多余键: %s' % extra)
    for n in nums:
        if n not in d: continue
        e = d[n]
        if not isinstance(e, dict): errs.append('%s 不是对象' % n); continue
        for k in ('stem_zh','ans_zh','com_zh','explain'):
            if k not in e: errs.append('%s 缺字段 %s' % (n,k)); continue
            if not isinstance(e[k], str): errs.append('%s.%s 非字符串' % (n,k))
        if not e.get('stem_zh','').strip(): errs.append('%s stem_zh 空' % n)
        if not e.get('ans_zh','').strip(): errs.append('%s ans_zh 空' % n)
        s = e.get('explain','')
        L = cn_len(s)
        if L < 80 or L > 250: errs.append('%s explain 中文字数 %d 越界' % (n,L))
        if '$' in s: errs.append('%s explain 含 $ 符号' % n)
        if '（⚠️待核）' in e.get('stem_zh','') or '（⚠️待核）' in e.get('ans_zh',''):
            print('待核:', n)
        if e.get('com_zh','') and src.get(n,{}).get('commentaire_fr','')=='' :
            errs.append('%s com_zh 非空但原文注释为空' % n)
    if errs:
        print('FAIL %d 个问题:' % len(errs))
        for x in errs[:40]: print(' -', x)
        sys.exit(1)
    print('OK %s: %d 条' % (path, len(d)))

main()
