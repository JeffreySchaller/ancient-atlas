#!/usr/bin/env python3
"""
set-interview.py — light up the Bernie Ong interview on release day.

    python3 scripts/set-interview.py dQw4w9WgXcQ
    python3 scripts/set-interview.py --clear      # back to the "coming" state

Writes the id into data/feature.json and rebuilds every surface that renders it,
so the creators hub and the homepage strip switch from placeholder to live embed
in one command. Nothing else needs touching on Saturday.

The id is validated before anything is written: an 11-character YouTube id, not
a full URL. Pasting a watch URL is the obvious mistake, so that is unpacked
rather than rejected.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
FEAT = ROOT / "data" / "feature.json"
ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def extract(arg):
    arg = arg.strip()
    m = re.search(r"(?:v=|youtu\.be/|embed/|shorts/)([A-Za-z0-9_-]{11})", arg)
    if m:
        return m.group(1)
    return arg


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    raw = sys.argv[1]
    cfg = json.loads(FEAT.read_text(encoding="utf-8"))

    if raw == "--clear":
        cfg["interview"]["id"] = ""
        cfg["interview"]["published"] = ""
        print("  · cleared — surfaces revert to the 'coming' state")
    else:
        vid = extract(raw)
        if not ID_RE.match(vid):
            sys.exit(f"ABORT: {vid!r} is not an 11-character YouTube id "
                     f"(paste the id or the full watch URL)")
        cfg["interview"]["id"] = vid
        from datetime import date
        cfg["interview"]["published"] = date.today().isoformat()
        print(f"  ✓ interview id set to {vid}")

    FEAT.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for script in ("build-creators-hub.py", "build-home-feature.py"):
        p = ROOT / "scripts" / script
        if not p.exists():
            continue
        r = subprocess.run([sys.executable, str(p)], cwd=ROOT, capture_output=True, text=True)
        print(r.stdout.rstrip() or r.stderr.rstrip())
        if r.returncode:
            sys.exit(f"ABORT: {script} failed")

    print("\nNext: python3 scripts/build-seo-pages.py, then commit and push.")


if __name__ == "__main__":
    main()
