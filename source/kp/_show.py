import json,sys
d=json.load(open('/home/thelia/Documents/radioamateur-fr/source/kp/in_5.json'))
ids=sys.argv[1:]
for x in d:
    if x['id'] not in ids: continue
    print('='*100)
    print(x['id'], x['anchor'], x['seclab'], '|', x['theme_fr'])
    print('--- COURS_FR ---')
    print(x.get('cours_fr') or '(vide)')
    print('--- SAMPLES (%d) ---'%len(x['samples']))
    for s in x['samples']:
        print('[%s] %s'%(s['num'], s['stem_fr']))
        for i,o in enumerate(s['options']):
            mark='*' if i==s.get('ans_idx') else ' '
            print('   %s %d) %s'%(mark,i+1,o))
        print('   =>',s.get('ans_fr'))
        if s.get('stem_zh'): print('   ZH:',s['stem_zh'])
        if s.get('commentaire_fr'): print('   COM:',s['commentaire_fr'])
