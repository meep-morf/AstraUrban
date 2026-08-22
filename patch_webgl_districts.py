#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
JS = ROOT / "_nuxt" / "u1ipQrxM.js"

REPS = [
    ("central-suburbs", "islamabad"),
    ("south-mumbai", "karachi"),
    ("western-suburbs", "lahore"),
    ("district-item-thane", "district-item-rawalpindi"),
    ("district-item-central-suburbs", "district-item-islamabad"),
    ("district-item-south-mumbai", "district-item-karachi"),
    ("district-item-western-suburbs", "district-item-lahore"),
]

text = JS.read_text(encoding="utf-8")
orig = text
for old, new in REPS:
    text = text.replace(old, new)
if text != orig:
    JS.write_text(text, encoding="utf-8")
    print("patched u1ipQrxM.js")
else:
    print("no changes")
