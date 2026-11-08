#!/usr/bin/env python3
"""Render the curated French vocabulary beside each lesson summary."""
import html
import json
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent
VOCAB = json.loads((BASE / 'lesson_vocab.json').read_text(encoding='utf-8'))
STYLE = '''<style id="lesson-vocab-style">
.lesson-vocab { border:1px solid #c9d9e5; border-radius:6px; background:#f5f9fc; padding:.7em 1em; margin:1em 0; }
.lesson-vocab p { margin:0 0 .35em; font-weight:bold; }
.lesson-vocab ul { margin:0; padding-left:1.4em; columns:2 18em; }
.lesson-vocab li { break-inside:avoid; }
</style>'''
SUMMARY = re.compile(r'<aside class="section-summary" data-section="(?P<id>[^"]+)"[^>]*>.*?</aside>', re.S)


def add_lesson_vocab(document):
    if 'id="lesson-vocab-style"' in document:
        raise ValueError('Lesson vocabulary is already present')
    seen = set()
    def insert(match):
        sid = match['id']
        if sid in seen or sid not in VOCAB:
            raise ValueError(f'Duplicate or missing lesson vocabulary: {sid}')
        seen.add(sid)
        entries = ''.join('<li><span lang="fr">' + html.escape(fr) + '</span>：' +
                          html.escape(zh) + '</li>' for fr, zh in VOCAB[sid])
        return (match[0] + '\n<aside class="lesson-vocab" data-section="' + sid +
                '" aria-label="本节必备法语词汇"><p>本节必备法语词汇</p><ul>' + entries + '</ul></aside>')
    document = SUMMARY.sub(insert, document)
    if seen != set(VOCAB):
        raise ValueError(f'Vocabulary sections do not match textbook: {sorted(set(VOCAB) - seen)}')
    if '</head>' not in document:
        raise ValueError('Missing HTML head')
    return document.replace('</head>', STYLE + '</head>', 1)
