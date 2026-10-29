import json,re,sys,glob
bad=0
for k in range(1,6):
    src=json.load(open(f'c7_{k}.json'))
    nums=[x['num'] for x in src]
    try:
        out=json.load(open(f'o7_{k}.json'))
    except Exception as e:
        print(f'chunk{k}: LOAD FAIL {e}'); bad+=1; continue
    miss=[n for n in nums if n not in out]; extra=[n for n in out if n not in nums]
    print(f'chunk{k}: keys={len(out)} miss={miss} extra={extra}')
    for x in src:
        n=x['num']
        if n not in out: continue
        o=out[n]
        for f in ('stem_zh','ans_zh','com_zh','explain'):
            if f not in o: print(f'  {n}: missing field {f}'); bad+=1
        e=o.get('explain','')
        L=len(re.findall(r'[\u4e00-\u9fff]',e))
        if L<80 or L>250: print(f'  {n}: explain cn-len={L}'); bad+=1
        blob=json.dumps(o,ensure_ascii=False)
        if '$' in blob: print(f'  {n}: DOLLAR'); bad+=1
        for m in re.findall(r'\d,\d+',blob): print(f'  {n}: comma-num {m}')
        if (x['commentaire_fr'].strip()=='') != (o.get('com_zh','').strip()==''):
            print(f'  {n}: com_zh emptiness mismatch (src={x["commentaire_fr"][:30]!r})')
        if not o.get('explain','') or '\\( ' not in o.get('explain','') and '\\(' not in o.get('explain',''):
            if '公式' not in o.get('explain',''):
                pass
print('issues flagged:',bad)
