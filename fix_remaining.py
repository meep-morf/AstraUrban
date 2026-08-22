#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPS = [
    ("faqs-hubtown", "faqs-astra-urban"),
    ("join hubtown and shape", "join Astra Urban and shape"),
    ("@hubtownlimitedd", "@astraurbanpk"),
    ("hubtownlimitedd", "astraurbanpk"),
    ("astra-vedant-sion-karachi-hubtown.avif", "astra-vedant-clifton-karachi.avif"),
    ('"name":"India","dial_code":"+92","code":"IN"', '"name":"Pakistan","dial_code":"+92","code":"PK"'),
    ("Real Estate Developer in India", "Real Estate Developer in Pakistan"),
    (r'replace(/\bhubtown\b/g,"")', r'replace(/\bastra-urban\b/g,"")'),
    ("> Loading content ", "> Loading Astra Urban "),
]

files = list(ROOT.rglob("*.html")) + list((ROOT / "_nuxt").glob("*.js"))
files += [ROOT / "sanity-assets.json", ROOT / "previews" / "comparison.json"]

for path in files:
    if "static-preview" in path.parts:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    orig = text
    for old, new in REPS:
        text = text.replace(old, new)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        print(f"fixed {path.relative_to(ROOT)}")
