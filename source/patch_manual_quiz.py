#!/usr/bin/env python3
"""Upgrade the edited manual's exercises without rebuilding its revised lessons."""
import json
from pathlib import Path
import re

from manual_quiz import QUIZ_CSS, QUIZ_SCRIPT, render_question

BASE = Path(__file__).resolve().parent
MANUAL = BASE.parent / 'manuel-zh.html'
QUESTION = re.compile(
    r'<li>\s*<p class="fr">(?P<stem>.*?)</p>'
    r'\s*<p class="zh[^\"]*">(?P<translation>.*?)</p>'
    r'\s*<p class="small question-number">.*?</p>'
    r'\s*<ol class="exam-options"[^>]*data-question="(?P<number>\d+)"[^>]*>.*?</ol>'
    r'\s*<details><summary>查看答案</summary>(?P<answer>.*?)</details>\s*</li>',
    re.S)


def main():
    original = MANUAL.read_text(encoding='utf-8')
    if 'id="manual-quiz-script"' in original:
        raise SystemExit('The manual already uses the card-style quiz renderer.')
    bank = json.loads((BASE / 'Exam1/questions/questions.json').read_text(encoding='utf-8'))
    questions = {q['num']: q for q in bank['questions']}
    count = 0

    def replace(match):
        nonlocal count
        count += 1
        return render_question(questions[match['number']], f'quiz-{count}',
                               stem_html=match['stem'], translation_html=match['translation'],
                               answer_html=match['answer'])

    updated = QUESTION.sub(replace, original)
    expected = original.count('<ol class="exam-options"')
    if count != expected or not count:
        raise ValueError(f'Only {count}/{expected} exercise blocks matched; refusing to write.')
    updated = updated.replace('</style>', QUIZ_CSS + '\n</style>', 1)
    updated = updated.replace('</body>', '<script id="manual-quiz-script">' + QUIZ_SCRIPT + '</script></body>', 1)
    updated = updated.replace('法语原题 + 中文 + 全部选项；答案已折叠，可先自测',
                              '默认显示法语、选项与题图；翻译、词汇和答案按需查看')
    updated = re.sub(
        r'(<div class="hd">高频考点：.*?</div>)',
        r'\1<p class="quiz-navigation-help">点击题框选中；方向键切换题目，'
        r'1–4 选择答案，C 查看本题翻译与词汇，X 切换本题题图，Z 展开本题解析。</p>', updated)
    MANUAL.write_text(updated, encoding='utf-8')
    print(f'Upgraded {count} questions with embedded images and card-style help.')


if __name__ == '__main__':
    main()
