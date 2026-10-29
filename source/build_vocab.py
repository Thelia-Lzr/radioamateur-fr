#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Construit la liste de candidats pour vocabulaire.csv :
# unigrammes + bigrammes/trigrammes issus de questions.json et de cours.txt,
# filtres des mots vides, fusionnes par frequence, plus une liste imposee.
import json, os, re, unicodedata, collections, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
from gen_common import load_questions, clean_cours      # noqa: E402

OUT = os.path.join(BASE, 'work')

STOP = set("""
le la les un une des du de d au aux et ou a en dans sur sous par pour avec sans
ce cet cette ces son sa ses leur leurs mon ma mes ton ta tes notre nos votre vos
il elle ils elles je tu nous vous on se que qui quoi dont ou est sont etre ete
ete ont avez avons ai as ayant sera seront soit fut quel quelle quels quelles
quand comment combien pourquoi si ne pas plus moins tres tout tous toute toutes
meme aussi alors donc car mais comme entre vers chez apres avant pendant depuis
encore deja oui non lors lorsque ainsi celui celle ceux y etc the of and to in
is are il-y-a qu-en qu-il l-a n-est c-est d-un d-une s-il j-ai peut peut-etre
doit doit-on faut il-faut veux voulez pouvez peut-on sais savez doit-il
laquelle lesquels lesquelles ceci cela ca ici la-bas alors ensuite puis aussi
environ toujours jamais rien autre autres chaque plusieurs certains quelque
afin dont lors quand numero n- 1 2 3 4 5 6 7 8 9 0
""".split())

# tournures de question : a exclure (ce ne sont pas des notions a apprendre)
SCAFFOLD = set("""
commence commence-par contactez contacte contactez-vous est-il est-elle sont-ils
etes-vous etes traduit-on signifie siginifie indique indiquer donne donner
relever relevez repondre repondez dites dire cochez choisir choisissez
quelle-est quel-est lequel-la combien-de a-quoi de-quoi dans-quel dans-quelle
la frequence la bande la puissance la tension la resistance le prefixe le
prefixe l-indicatif une-bande un-radioamateur vous-contactez dont-le
vrai vraie fausse exacte exact suivante suivantes proposition propositions
reponse reponses question questions affirmation affirmations
""".split())

# liste imposee : notions incontournables (reglementation + technique)
IMPOSE = [
    # reglementation / administratif
    "arrêté", "arrêté du 21 septembre 2000", "décret", "décision", "dérogation",
    "délivrance", "titulaire", "précaire et révocable", "à égalité de droit",
    "primaire", "secondaire", "statut primaire", "statut secondaire",
    "attribution", "autorisation", "certificat d'opérateur", "indicatif d'appel",
    "préfixe", "suffixe", "France métropolitaine", "départements d'outre-mer",
    "collectivités d'outre-mer", "ANFR", "Arcep", "ARCOM", "UIT", "CEPT", "HAREC",
    "Règlement des radiocommunications", "service amateur", "service d'amateur par satellite",
    "sanction", "suspension", "retrait", "amende", "infraction", "manquement",
    "brouillage", "brouillage préjudiciable", "perturbation", "plainte",
    "carnet de station", "journal de bord", "déclaration", "téléservice",
    "puissance apparente rayonnée", "PIRE", "PAR", "largeur de bande",
    "bande passante", "classe d'émission", "modulation d'amplitude",
    "modulation de fréquence", "bande latérale unique", "télégraphie",
    "exploitation", "station", "station fixe", "station mobile",
    "convocation", "épreuve", "examen", "moyenne", "note", "résultat",
    # Q code et alphabet
    "QRA", "QRG", "QRH", "QRK", "QRL", "QRM", "QRN", "QRO", "QRP", "QRT",
    "QRU", "QRV", "QRX", "QRZ", "QSA", "QSB", "QSL", "QSO", "QSP", "QSY",
    "QTH", "QTR", "RST", "ALFA", "BRAVO", "CHARLIE", "DELTA", "ECHO", "FOX-TROT",
    "GOLF", "HOTEL", "INDIA", "JULIETT", "KILO", "LIMA", "MIKE", "NOVEMBER",
    "OSCAR", "PAPA", "QUEBEC", "ROMEO", "SIERRA", "TANGO", "UNIFORM", "VICTOR",
    "WHISKEY", "X-RAY", "YANKEE", "ZOULOU", "Zulu",
    # technique
    "antenne", "antenne doublet", "demi-onde", "quart d'onde", "antenne Yagi",
    "gain", "directivité", "diagramme de rayonnement", "angle d'ouverture",
    "impédance", "impédance caractéristique", "adaptation", "désadaptation",
    "ondes stationnaires", "ROS", "TOS", "coefficient de réflexion",
    "ligne de transmission", "câble coaxial", "ligne bifilaire", "affaiblissement",
    "propagation", "ionosphère", "onde réfléchie", "onde de sol", "MUF",
    "fréquence", "longueur d'onde", "décibel", "rapport", "atténuation",
    "résistance", "condensateur", "bobine", "self", "inductance", "capacité",
    "transformateur", "diode", "transistor", "amplificateur opérationnel",
    "filtre", "filtre passe-bas", "filtre passe-bande", "résonance",
    "facteur de qualité", "oscillateur", "mélangeur", "modulateur",
    "fréquence intermédiaire", "fréquence image", "sélectivité", "sensibilité",
    "émetteur", "récepteur", "transceiver", "alimentation", "redressement",
    "code des couleurs", "tolérance", "multimètre", "voltmètre", "ampèremètre",
    "ohmmètre", "oscilloscope", "wattmètre", "TOS-mètre",
]

NUM = re.compile(r'^[0-9]+(?:[.,][0-9]+)?$')
TOKEN = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ'\-]*")

# fragments sans interet a l'extraction finale
JUNK = set("""
d'un d'une l'antenne l'indicatif l'impedance qu d'emission d'onde voir fait
partir passe deux cas exemple metropolitaine nom mes qu'il qu'elle n'y
s'agit ainsi voici voila soit avoir etre celui celle ceux dessus dessous
entre autres tel telle tous toute meme aussi donc alors puis quand comment
""".split())


def strip_acc(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


def norm_tok(t):
    return strip_acc(t.lower()).strip("-'")


def tok_ok(t):
    k = norm_tok(t)
    if not k or len(k) < 2 or k in STOP or k in SCAFFOLD or NUM.match(k):
        return None
    if k.startswith("l-") or k.startswith("d-") or k.startswith("qu-"):
        return None
    return k


def collect():
    uni = collections.Counter()      # clef sans accent -> freq
    forms = {}                       # clef -> meilleure graphie
    bi = collections.Counter()
    corpus = []
    for q in load_questions()['questions']:
        corpus.append(q['question'])
        corpus.extend(q['propositions'])
    for _, p in clean_cours():
        corpus.append(p)
    for txt in corpus:
        toks = TOKEN.findall(txt)
        lows = [t.lower() for t in toks]
        for t in toks:
            k = tok_ok(t)
            if not k:
                continue
            uni[k] += 1
            if k not in forms or (t.islower() and not forms[k].islower()):
                forms[k] = t
        for n in (2, 3):
            for i in range(len(lows) - n + 1):
                g = lows[i:i + n]
                if any(NUM.match(x) for x in g):
                    continue
                k = ' '.join(norm_tok(x) for x in g)
                ks = k.split()
                if len(ks) != n or all(x in STOP for x in ks):
                    continue
                if ks[0] in STOP or ks[-1] in STOP:
                    continue
                if any(x in SCAFFOLD for x in ks):
                    continue
                if any(x in STOP for x in ks):
                    continue
                if any(len(x) < 2 for x in ks):
                    continue
                bi[k] += 1
    return uni, forms, bi


def main():
    os.makedirs(OUT, exist_ok=True)
    uni, forms, bi = collect()
    cand = []
    seen = set()
    for k, n in uni.most_common(900):
        if n < 3:
            break
        cand.append((k, forms.get(k, k), n))
        seen.add(k)
    # mots composees frequent (au moins 8 occurrences)
    comp = [(k, k, n) for k, n in bi.most_common(320) if n >= 8]
    out = []
    for k, form, n in cand + comp:
        if k in JUNK or k.startswith("l'") or k.startswith("d'") or k.startswith("qu"):
            continue
        out.append({'key': k, 'form': form, 'freq': n})
    # ajout de la liste imposee (freq 0 si jamais vue)
    for t in IMPOSE:
        k = norm_tok(t)
        if k in seen:
            continue
        seen.add(k)
        out.append({'key': k, 'form': t, 'freq': uni.get(k, 0)})
    out.sort(key=lambda d: (-d['freq'], d['key']))
    with open(os.path.join(OUT, 'vocab_candidates.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=0)
    print('candidats :', len(out))
    # decoupage en 3 lots equilibres
    third = (len(out) + 2) // 3
    for i in range(3):
        chunk = out[i * third:(i + 1) * third]
        with open(os.path.join(OUT, 'vocab_part%d.json' % (i + 1)), 'w', encoding='utf-8') as f:
            json.dump(chunk, f, ensure_ascii=False, indent=1)
        print('part%d : %d entrees (freq %d..%d)'
              % (i + 1, len(chunk), chunk[-1]['freq'] if chunk else 0,
                 chunk[0]['freq'] if chunk else 0))


if __name__ == '__main__':
    main()
