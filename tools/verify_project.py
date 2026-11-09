#!/usr/bin/env python3
"""Validate the delivered textbook and assets without rebuilding or changing them."""
import base64
import csv
import json
from pathlib import Path
import re
import sys
import zipfile
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "source"))
from gen_common import section_questions

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent


def main():
    document = (ROOT / 'manuel-zh.html').read_text(encoding='utf-8')
    soup = BeautifulSoup(document, 'html.parser')
    assert len(soup.select('#study-sidebar')) == 1
    assert soup.select_one('main .toc') is None, '目录不应留在正文'
    assert len(soup.select('#study-sidebar .toc-chapter')) == 18
    assert soup.select_one('#study-sidebar [data-mistake-link="mistake-book.html"]') is not None
    from study_navigation import add_study_navigation
    assert add_study_navigation(document) == document, '重复更新导航应保持成品不变'
    plan = json.loads((ROOT / 'source/plan.json').read_text(encoding='utf-8'))
    guide = json.loads((ROOT / 'source/study_guide.json').read_text(encoding='utf-8'))
    bank = json.loads((ROOT / 'source/Exam1/questions/questions.json').read_text(encoding='utf-8'))
    by_number = {q['num']: q for q in bank['questions']}
    expected = sum(len(unit.get('picks', [])) for unit in plan['units'])
    questions = soup.select('.exam-question')
    assert expected == 455, '默认例题数量不匹配'
    assert len(questions) == sum(unit['nq'] for unit in plan['units']) == 2688, '课后题总数不匹配'
    for unit in plan['units']:
        heading = soup.find('h3', id=unit['id'])
        section_nodes = []
        for sibling in heading.next_siblings:
            if getattr(sibling, 'name', None) in ('h2', 'h3'):
                break
            if getattr(sibling, 'name', None):
                section_nodes.extend(sibling.select('.exam-question'))
        actual = [q['data-question'] for q in section_nodes]
        wanted = [str(q['num']) for q in section_questions(unit.get('anchors', []))]
        assert len(actual) == len(set(actual)) and set(actual) == set(wanted), unit['id']
        examples = [str(q['num']) for q in unit.get('picks', [])]
        assert actual[:len(examples)] == examples, unit['id']
        for q in section_nodes[:len(examples)]:
            assert q.find_parent('details', class_='all-lesson-questions') is None, unit['id']
        for q in section_nodes[len(examples):]:
            container = q.find_parent('details', class_='all-lesson-questions')
            assert container is not None and not container.has_attr('open'), unit['id']
    assert len(soup.select('.chapter-summary')) == len(guide['chapters']) == 18
    assert len(soup.select('.section-summary')) == len(guide['sections']) == 126
    vocabulary_by_section = json.loads((ROOT / 'source/lesson_vocab.json').read_text(encoding='utf-8'))
    vocabulary_blocks = soup.select('.lesson-vocab')
    assert len(vocabulary_blocks) == len(vocabulary_by_section) == 126
    assert {block['data-section'] for block in vocabulary_blocks} == set(guide['sections'])
    for block in vocabulary_blocks:
        sid = block['data-section']
        assert block.find_previous_sibling()['data-section'] == sid
        assert len(block.select('li')) >= len(vocabulary_by_section[sid]) >= 3
        assert all(item.select_one('[lang="fr"]') for item in block.select('li'))
    sourced_vocab = json.loads((ROOT / 'source/question_vocab.json').read_text(encoding='utf-8'))
    glossary = json.loads((ROOT / 'source/alphabetical_vocab.json').read_text(encoding='utf-8'))
    assert len(soup.select('.memory-card')) == 18
    assert len(soup.select('.memory-section')) == 126
    section_cards = soup.select('.section-memory-card')
    assert len(section_cards) == 126, '每小节必须有独立速记卡'
    assert {card['data-section'] for card in section_cards} == set(guide['sections'])
    for card in section_cards:
        sid = card['data-section']
        previous = card.find_previous_sibling()
        assert 'lesson-vocab' in previous.get('class', []) and previous['data-section'] == sid, sid
        following = card.find_next_sibling()
        assert following and 'exam' in following.get('class', []), f'{sid}: 速记卡应在习题之前'
        assert card.find_parent(class_='memory-card') is None, sid
        assert len(card.select('.memory-node')) == 3, sid
        assert not any(node.has_attr('open') for node in card.select('details')), sid
    assert len(soup.select('.memory-section-link')) == 126
    assert len(soup.select('.memory-answer')) == 2688
    assert len(soup.select('.glossary-entry')) == len(glossary)
    assert all(len(card.select('.memory-node')) >= 3 for card in soup.select('.memory-card'))
    assert all(not details.has_attr('open') for details in soup.select('.memory-review'))
    from build_learning_vocab import key, occurs
    assert glossary == sorted(glossary, key=lambda e: (key(e['fr']), e['fr']))
    for unit in plan['units']:
        sid = unit['id']
        wanted = {str(q['num']) for q in section_questions(unit['anchors'])}
        panel = soup.select_one('.memory-section[data-section="' + sid + '"]')
        assert {q['data-question'] for q in panel.select('.memory-answer')} == wanted, sid
        for entry in sourced_vocab[sid]:
            assert entry['questions'] and set(entry['questions']) <= wanted, (sid, entry['fr'])
            forms = entry['note'][5:].split('、') if entry['note'].startswith('题中形式：') else [entry['fr']]
            for number in entry['questions']:
                q = by_number[number]
                text = q['question'] + ' ' + ' '.join(q['propositions'])
                assert any(occurs(form,text) for form in forms), (sid,entry['fr'],number)
    assert all(body.select('.exam-key') for body in soup.select('.lesson-body'))
    ids = [tag['id'] for tag in soup.select('[id]')]
    assert len(ids) == len(set(ids)), '存在重复锚点'
    missing = {a['href'][1:] for a in soup.select('a[href^="#"]')} - set(ids)
    assert not missing, f'损坏的章节链接：{sorted(missing)}'
    normalize = lambda s: re.sub(r'\s+', ' ', s).strip()
    for question in questions:
        number = question['data-question']
        source = by_number[number]
        mark = question.select_one('[data-action="mistake"]')
        assert mark is not None and mark.get('aria-pressed') == 'false', number
        options = question.select('.quiz-choice')
        assert len(options) == 4, number
        assert [normalize(n.get_text('\n')) for n in question.select('.quiz-choice-fr')] == [
            normalize(p) for p in source['propositions']], number
        assert len(question.select('.quiz-choice[data-ok="1"]')) == 1, number
        assert options[source['reponse']].get('data-ok') == '1', number
        assert all(n.has_attr('hidden') for n in question.select('.quiz-tr')), number
        assert not question.select_one('.quiz-answer').has_attr('open'), number
        wrapper = question.select_one('.quiz-image')
        assert question.find(recursive=False) is wrapper, f'题图不在最上方：{number}'
        assert not wrapper.has_attr('hidden'), number
        image = wrapper.find('img')
        assert int(image['width']) > 0 and int(image['height']) > 0, number
        assert image['src'].startswith('data:image/png;base64,'), number
        assert base64.b64decode(image['src'].split(',', 1)[1]) == (
            ROOT / f'source/Exam1/questions/{number}.png').read_bytes(), number
    notebook = (ROOT / 'mistake-book.html').read_text(encoding='utf-8')
    assert 'data-mistake-book' in notebook and 'id="mistake-bank"' in notebook
    notebook_questions = re.findall(r'<li class="exam-question"[^>]*>.*?</details>\s*</li>', notebook, re.S)
    manual_questions = re.findall(r'<li class="exam-question"[^>]*>.*?</details>\s*</li>', document, re.S)
    assert notebook_questions == manual_questions, '错题本题目与教材不同步'
    mock_exam = (ROOT / 'mock-exam.html').read_text(encoding='utf-8')
    exam_questions = re.findall(r'<li class="exam-question"[^>]*>.*?</details>\s*</li>', mock_exam, re.S)
    assert exam_questions == manual_questions, '模拟考试题目与教材不同步'
    manifest = json.loads(re.search(r'<script id="mock-exam-data" type="application/json">(.*?)</script>', mock_exam, re.S)[1])
    assert len(manifest['questions']) == len(questions) == 2688
    assert {q['id'] for q in manifest['questions']} == {q['data-question'] for q in questions}
    assert manifest['modes']['regulation']['seconds'] == 900
    assert manifest['modes']['technique']['seconds'] == 1800
    assert all(len(mode['themes']) == 10 for mode in manifest['modes'].values())
    assert len(manifest['modes']['regulation']['chapters']) == 5
    assert len(manifest['modes']['technique']['chapters']) == 13
    for q in manifest['questions']:
        assert q['theme'] == by_number[q['id']]['themeNum'] and q['answer'] == by_number[q['id']]['reponse']
    assert soup.select_one('.sidebar-shortcuts [data-mistake-link="mistake-book.html"]').find_next_sibling()['data-mistake-link'] == 'mock-exam.html'
    assert soup.find(id='quiz-mistakes-script') is not None
    script = soup.find(id='manual-quiz-script').get_text()
    for key in ('c', 'x', 'z', 'arrowdown', 'arrowup'):
        assert f"key === '{key}'" in script, key
    assert 'quiz-feedback' not in document, '已删除的文字反馈不应重新出现'
    with (ROOT / 'data/vocabulaire.csv').open(encoding='utf-8', newline='') as source:
        vocabulary = list(csv.reader(source))
    assert len(vocabulary) - 1 == 1069, '词表数量不匹配'
    decks = sorted((ROOT / 'decks').glob('*.apkg'))
    assert len(decks) == 8, '卡包缺失'
    for path in decks:
        with zipfile.ZipFile(path) as package:
            assert package.testzip() is None, f'卡包损坏：{path.name}'
            assert any(n.startswith('collection.') for n in package.namelist()), path.name
    for path in [ROOT / 'README.md', *sorted((ROOT / 'docs').glob('*.md'))]:
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if re.match(r'(?:https?://|#)', target):
                continue
            local = target.split('#', 1)[0]
            assert (path.parent / local).exists(), f'{path.name}: {target}'
    print(f'通过：18 章 / 126 节 / {len(questions)} 道关联习题（默认显示 {expected} 道例题），题图、选项、默认状态、快捷键与锚点完整。')
    print(f'通过：126 张小节速记卡 + 18 张章末速记卡 / 2688 条逐题解题依据 / {len(glossary)} 条字母序词汇；题源词汇、排序与链接完整。')
    print(f'通过：{len(vocabulary)-1} 条原词汇、{len(decks)} 个 Anki 包与文档链接完整。')


if __name__ == '__main__':
    try:
        main()
    except (AssertionError, KeyError, FileNotFoundError, zipfile.BadZipFile) as error:
        print(f'检查失败：{error}', file=sys.stderr)
        sys.exit(1)
