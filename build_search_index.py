#!/usr/bin/env python3
"""Build the lightweight cross-phase topic search index for the Telugu roadmap."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOPIC_RE = re.compile(r'(<details\s+class="t"[^>]*>\s*<summary>)(.*?)(</summary>)', re.S)
TAG_RE = re.compile(r'<[^>]+>')
ANCHOR_RE = re.compile(r'<span class="global-search-anchor" id="global-topic-\d+-\d+"></span>')


def plain(value: str) -> str:
    return ' '.join(html.unescape(TAG_RE.sub(' ', value)).split())


items = []
for phase in range(1, 9):
    path = ROOT / f'telugu-phase-{phase}.html'
    source = ANCHOR_RE.sub('', path.read_text(encoding='utf-8'))
    counter = [0]

    def index_topic(match):
        counter[0] += 1
        summary = match.group(2)
        title = plain(re.sub(r'<small>.*?</small>', '', summary, flags=re.S))
        subtitle_match = re.search(r'<small>(.*?)</small>', summary, re.S)
        subtitle = plain(subtitle_match.group(1)) if subtitle_match else ''
        topic_id = f'global-topic-{phase}-{counter[0]}'
        items.append({
            'phase': phase,
            'title': title,
            'subtitle': subtitle,
            'href': f'telugu-phase-{phase}.html#{topic_id}',
        })
        return f'<span class="global-search-anchor" id="{topic_id}"></span>' + match.group(1) + summary + match.group(3)

    source = TOPIC_RE.sub(index_topic, source)
    path.write_text(source, encoding='utf-8')

(ROOT / 'global-search-index.json').write_text(
    json.dumps(items, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8'
)
print(f'Indexed {len(items)} topics across 8 phases.')
