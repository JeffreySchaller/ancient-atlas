#!/usr/bin/env python3
"""Keep the optional GA4 loader on all published HTML pages. Idempotent."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SNIPPET = '<script defer src="/assets/js/analytics.js"></script>'
def install():
    count = 0
    for path in (ROOT / 'public').rglob('*.html'):
        text = path.read_text(encoding='utf-8')
        if SNIPPET in text or '</head>' not in text:
            continue
        path.write_text(text.replace('</head>', SNIPPET + '\n</head>', 1), encoding='utf-8')
        count += 1
    print(f'GA4 loader added to {count} pages; GoatCounter unchanged.')
if __name__ == '__main__':
    install()
