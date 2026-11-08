"""Build sourced lesson vocabulary and an alphabetical glossary from local exam text."""
import csv
from collections import Counter
import json
from pathlib import Path
import re
import unicodedata
from gen_common import section_questions, load_questions

BASE = Path(__file__).resolve().parent

def key(value):
    return ''.join(c for c in unicodedata.normalize('NFD', value.casefold().replace('’', "'")) if not unicodedata.combining(c))

def occurs(term, text):
    return re.search(r'(?<!\w)' + re.escape(key(term)) + r'(?!\w)', key(text)) is not None

# Infinitives plus forms actually searched in the question stems and choices.
VERBS = [
 ('atténuer','衰减；减弱','atténue|atténuer'),
 ('attribuer','划分；指配；授予','attribuer|attribué|attribuée|attribuées'),
 ('brouiller','干扰','brouiller|brouille|brouillé'),
 ('cesser','停止','cesser|cesse'),
 ('commuter','切换；换接','commuter|commute'),
 ('convertir','转换','convertir|convertit|converti'),
 ('déclarer','申报','déclarer|déclare|déclarée'),
 ('délivrer','签发；发放','délivrer|délivre|délivré|délivrée'),
 ('dépendre de','取决于','dépend|dépendent|dépendre'),
 ('dépasser','超过；超出','dépasser|dépasse|dépassé'),
 ('déterminer','确定；求出','déterminer|détermine|déterminée'),
 ('dissiper','耗散','dissiper|dissipe|dissipée'),
 ('émettre','发射','émettre|émet|émettent|émettant'),
 ('engendrer','产生；引起','engendrer|engendre|engendré'),
 ('entraîner','导致；引起','entraîner|entraîne|entraine|entraîne-t-il'),
 ('éviter','避免','éviter|évite'),
 ('fournir','提供；供给','fournir|fournit|fournie'),
 ('induire','感应产生；引起','induire|induit|induite'),
 ('nécessiter','需要；要求','nécessite|nécessiter|nécessitent'),
 ('prévoir','规定；预见','prévoit|prévoir|prévu|prévue'),
 ('rayonner','辐射','rayonner|rayonne|rayonnée|rayonné'),
 ('redresser','整流','redresser|redresse|redressée'),
 ('repérer','标出；识别','repérer|repéré|repérée'),
 ('retransmettre','转发；转播','retransmettre|retransmet'),
 ('supprimer','消除；抑制','supprimer|supprime|supprimée|supprimé'),
 ('transmettre','传输；发送','transmettre|transmet|transmis|transmise'),
 ('accorder','调谐；授予','accorder|accordé|accordée'),
 ('adapter','匹配；适配','adapter|adaptée|adapté'),
]

def build():
    bank = load_questions()['questions']
    texts = {q['num']: q['question'] + '\n' + '\n'.join(q['propositions']) for q in bank}
    normalized_texts = {n:key(t) for n,t in texts.items()}
    def matches(term):
        pattern = re.compile(r'(?<!\w)' + re.escape(key(term)) + r'(?!\w)')
        return [n for n,t in normalized_texts.items() if pattern.search(t)]
    glossary = []
    for row in csv.DictReader((BASE.parent / 'data/vocabulaire.csv').open(encoding='utf-8')):
        examples = matches(row['Français'])
        glossary.append(dict(fr=row['Français'], zh=row['中文'], category=row['词性/类别'],
                             note=row['备注'], questions=examples))
    for fr,zh,forms in VERBS:
        matched = [(n,f) for f in forms.split('|') for n in matches(f)]
        if matched:
            entry = next((e for e in glossary if key(e['fr']) == key(fr)), None)
            if entry is None:
                entry = dict(fr=fr, zh=zh, category='动词', note='', questions=[]); glossary.append(entry)
            entry.update(zh=zh, category='动词', questions=[n for n,f in matched],
                         note='题中形式：' + '、'.join(sorted({f for n,f in matched})))
    glossary.sort(key=lambda e:(key(e['fr']), e['fr']))
    qv = json.loads((BASE / 'q_vocab.json').read_text(encoding='utf-8'))
    units = json.loads((BASE / 'plan.json').read_text(encoding='utf-8'))['units']
    lessons = {}
    for u in units:
        nums = [q['num'] for q in section_questions(u['anchors'])]
        count = Counter(key(e['fr']) for n in nums for e in qv.get(n, []))
        candidates = []
        for e in glossary:
            found = [n for n in nums if n in e['questions']]
            if found:
                candidates.append(dict(e, questions=found))
        # Prefer question-linked terminology, reserve space for exam verbs.
        candidates.sort(key=lambda e:(-count[key(e['fr'])], -len(e['questions']), key(e['fr'])))
        terms = [e for e in candidates if '动词' not in e['category']][:16]
        verbs = [e for e in candidates if '动词' in e['category']][:5]
        lessons[u['id']] = terms + verbs
    (BASE / 'question_vocab.json').write_text(json.dumps(lessons,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (BASE / 'alphabetical_vocab.json').write_text(json.dumps(glossary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('词表',len(glossary),'每节题源词汇',sum(map(len,lessons.values())))

if __name__ == '__main__':
    build()
