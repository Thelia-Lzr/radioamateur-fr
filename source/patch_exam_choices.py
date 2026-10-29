#!/usr/bin/env python3
"""Add source choices in place, preserving the manual's later editorial fixes."""
import collections
import difflib
import html
import json
from pathlib import Path
import re

from gen_manuel import CSS, question_options

BASE = Path(__file__).resolve().parent
MANUAL = BASE.parent / 'manuel-zh.html'
TOKEN = re.compile(
    r'<h3 id="(?P<section>[^"]+)">|'
    r'(?P<question><li>\s*<p class="fr">(?P<text>.*?)</p>'
    r'\s*<p class="zh[^\"]*">.*?</p>\s*)'
    r'(?P<answer><details><summary>查看答案</summary>\s*'
    r'<p class="ans">✔ 正确答案：)', re.S)


def normalize(value):
    value = re.sub(r'<br\s*/?>', '\n', value)
    return re.sub(r'\s+', ' ', html.unescape(value)).strip()


def main():
    original = MANUAL.read_text(encoding='utf-8')
    if 'class="exam-options"' in original:
        raise SystemExit('Choices are already present; no changes made.')
    plan = json.loads((BASE / 'plan.json').read_text(encoding='utf-8'))
    picks = {u['id']: u.get('picks', []) for u in plan['units']}
    counts = collections.Counter()
    section = None

    def replace(match):
        nonlocal section
        if match['section']:
            section = match['section']
            return match[0]
        q = picks[section][counts[section]]
        # A few questions have since gained LaTeX formatting. Check similarity
        # before using their section and position as the stable identifier.
        similarity = difflib.SequenceMatcher(
            None, normalize(match['text']), normalize(q['question'])).ratio()
        if similarity < 0.75:
            raise ValueError(f'Question mismatch in {section}: {q["num"]}')
        counts[section] += 1
        return (match['question'] + question_options(q) + '\n'
                + match['answer'] + chr(ord('A') + q['reponse']) + ' — ')

    updated = TOKEN.sub(replace, original)
    for sid, questions in picks.items():
        if counts[sid] != len(questions):
            raise ValueError(f'Incomplete section {sid}: {counts[sid]}/{len(questions)}')
    # Reuse only the new choice styles, leaving all existing math styles intact.
    new_styles = CSS[CSS.index('.exam .exam-options'):CSS.index('.fr {')]
    updated = updated.replace('</style>', new_styles + '\n</style>', 1)
    updated = updated.replace('法语原题 + 中文 + 答案，答案已折叠，可先自测',
                              '法语原题 + 中文 + 全部选项；答案已折叠，可先自测')
    updated = updated.replace(
        '可在 <code>questions.json</code> 里按题号检索原题与全部选项。',
        '全部选项已按题库原顺序列出，先作答，再展开查看答案。')
    MANUAL.write_text(updated, encoding='utf-8')
    print(f'Added choices to {sum(counts.values())} questions in {len(counts)} sections.')


if __name__ == '__main__':
    main()
