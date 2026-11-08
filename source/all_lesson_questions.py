"""Add the remaining Exam'1 questions to each lesson without replacing the manual."""
import html
import re
from gen_common import section_questions
from manual_quiz import render_question

MARKER = '<p class="small">题号为 Exam\'1 题库中的 <code>num</code>；'


def add_all_lesson_questions(document, units):
    for unit in units:
        questions = section_questions(unit.get('anchors', []))
        if len(questions) != unit['nq']:
            raise ValueError(f"Question count mismatch: {unit['id']}")
        picked = {str(q['num']) for q in unit.get('picks', [])}
        remaining = [q for q in questions if str(q['num']) not in picked]
        if not picked.issubset({str(q['num']) for q in questions}):
            raise ValueError(f"Example not linked to lesson: {unit['id']}")
        if not remaining:
            continue
        heading = re.search(r'<h3 id="' + re.escape(unit['id']) + r'"[^>]*>', document)
        if not heading:
            raise ValueError(f"Lesson not found: {unit['id']}")
        end = re.search(r'<h[23](?:\s|>)', document[heading.end():])
        end_pos = heading.end() + end.start() if end else len(document)
        section = document[heading.start():end_pos]
        if section.count(MARKER) != 1:
            raise ValueError(f"Exercise insertion point missing: {unit['id']}")
        sid = html.escape(unit['id'], quote=True)
        extra = ('<details class="all-lesson-questions"><summary>展开其余 '
                 + str(len(remaining)) + ' 道相关题目（本节共 ' + str(len(questions))
                 + ' 道）</summary><ol start="' + str(len(picked) + 1) + '">\n'
                 + '\n'.join(render_question(q, 'quiz-' + sid + '-' + str(q['num']))
                             for q in remaining) + '\n</ol></details>\n')
        section = section.replace(MARKER, extra + MARKER, 1)
        document = document[:heading.start()] + section + document[end_pos:]
    return document
