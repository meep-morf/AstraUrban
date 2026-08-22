#!/usr/bin/env python3
"""Finish remaining Astra Urban Pakistan branding gaps."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ADDRESS = "Suite 1204, Ocean Tower, Clifton Block 5, Karachi 75600, Pakistan"
OLD_HUBTOWN_ADDR = (
    "HUBTOWN SEASONS, CTS No. 469-A, OPP. JAIN TEMPLE, R.K. CHEMBURKAR MARG, "
    "CHEMBUR EAST, Karachi Suburban, Sindh, 400071"
)

LETTERS_BLOCK = """<g class="letters" data-v-f17dfb82><g transform="translate(0,0) scale(8)" data-v-f17dfb82><rect id="H_C1col" class="cell" x="0" y="0" width="1" height="1" data-v-f17dfb82></rect><rect id="H_C5col" class="cell" x="4" y="0" width="1" height="1" data-v-f17dfb82></rect><rect id="H_C1row" class="cell" x="2" y="2" width="1" height="1" data-v-f17dfb82></rect><path class="stroke" d="M0.5 0.5L2.5 4.5" pathLength="1" data-v-f17dfb82></path><path class="stroke" d="M4.5 0.5L2.5 4.5" pathLength="1" data-v-f17dfb82></path></g><g transform="translate(52,0) scale(8)" data-v-f17dfb82><rect id="U_C1col" class="cell" x="0" y="2" width="1" height="1" data-v-f17dfb82></rect><rect id="U_C5col" class="cell" x="4" y="2" width="1" height="1" data-v-f17dfb82></rect><rect id="U_E1row" class="cell" x="0" y="4" width="1" height="1" data-v-f17dfb82></rect><path class="stroke" d="M4.5 0.5L0.5 0.5L0.5 2.5L4.5 2.5L4.5 4.5L0.5 4.5" pathLength="1" data-v-f17dfb82></path></g><g transform="translate(104,0) scale(8)" data-v-f17dfb82><rect class="cell" x="2" y="0" width="1" height="1" data-v-f17dfb82></rect><path id="B_mid" class="stroke" d="M2.5 0.5L2.5 4.5" pathLength="1" data-v-f17dfb82></path><path id="B_loopBottom" class="stroke" d="M0.5 0.5L4.5 0.5" pathLength="1" data-v-f17dfb82></path><path id="B_loopTop" class="stroke" d="M0.5 0.5L4.5 0.5" pathLength="1" data-v-f17dfb82></path></g><g transform="translate(156,0) scale(8)" data-v-f17dfb82><rect id="T_C3col" class="cell" x="2" y="0" width="1" height="1" data-v-f17dfb82></rect><rect id="T_A3row" class="cell" x="0" y="0" width="1" height="1" data-v-f17dfb82></rect><path class="stroke" d="M4.5 0.5L4.5 4.5L0.5 4.5" pathLength="1" data-v-f17dfb82></path></g><g transform="translate(208,0) scale(8)" data-v-f17dfb82><rect class="cell" x="0" y="0" width="1" height="1" data-v-f17dfb82></rect><rect class="cell" x="4" y="0" width="1" height="1" data-v-f17dfb82></rect><path id="O_triangle" d="M0.5 1L0.5 5L5 5Z" data-v-f17dfb82></path><path class="stroke" d="M0.5 0.5L2.5 4.5" pathLength="1" data-v-f17dfb82></path><path class="stroke" d="M4.5 0.5L2.5 4.5" pathLength="1" data-v-f17dfb82></path></g><g transform="translate(260,0) scale(8)" data-v-f17dfb82><rect id="W_C1col" class="cell" x="0" y="0" width="1" height="1" data-v-f17dfb82></rect><rect id="W_C5col" class="cell" x="4" y="0" width="1" height="1" data-v-f17dfb82></rect><rect id="W_E1row" class="cell" x="0" y="2" width="1" height="1" data-v-f17dfb82></rect><rect id="W_A3col" class="cell" x="2" y="2" width="1" height="1" data-v-f17dfb82></rect><path class="stroke" d="M0.5 0.5L0.5 4.5L4.5 4.5" pathLength="1" data-v-f17dfb82></path></g><g transform="translate(312,0) scale(8)" data-v-f17dfb82><rect id="N_C1col" class="cell" x="0" y="0" width="1" height="1" data-v-f17dfb82></rect><rect id="N_C5col" class="cell" x="4" y="0" width="1" height="1" data-v-f17dfb82></rect><rect id="N_A5row" class="cell" x="4" y="2" width="1" height="1" data-v-f17dfb82></rect><path class="stroke" d="M4.5 0.5L0.5 4.5" pathLength="1" data-v-f17dfb82></path></g></g>"""

CONTENT_REPS = [
    (OLD_HUBTOWN_ADDR, ADDRESS),
    (
        "HUBTOWN SEASONS, CTS No. 469-A, OPP. JAIN TEMPLE, R.K. CHEMBURKAR MARG, CHEMBUR EAST, Mumbai Suburban,\nMaharashtra, 400071",
        ADDRESS,
    ),
    (
        "HUBTOWN SEASONS, CTS No. 469-A, OPP. JAIN TEMPLE, R.K. CHEMBURKAR MARG, CHEMBUR EAST, Karachi Suburban,\nSindh, 400071",
        ADDRESS,
    ),
    ("HUBTOWN SEASONS", "Astra Urban Tower"),
    ("HUBTOWN Aditya", "Astra Aditya"),
    ("HUBTOWN", "Astra Urban"),
    ("HUBTOWN", "Astra Urban"),
    (">India (+92)<", ">Pakistan (+92)<"),
    ('"India (+92)"', '"Pakistan (+92)"'),
    ("district-item-thane", "district-item-rawalpindi"),
    ("district-item-central-suburbs", "district-item-islamabad"),
    ("district-item-south-mumbai", "district-item-karachi"),
    ("district-item-western-suburbs", "district-item-lahore"),
]

ASSET_REPS = [
    ("HUBTOWN", "Astra Urban"),
    ("hubtown_", "astra-"),
    ("hubtown-", "astra-"),
    ("akruti ", "astra "),
    ("Akruti ", "Astra "),
    ("Ackruti ", "Astra "),
    ("India International Tower", "Ocean Tower Clifton"),
    ("mumbai-hubtown", "karachi-astra"),
    ("-mumbai-", "-karachi-"),
]


def replace_loader_letters(text: str) -> str:
    pattern = r'<g class="letters" data-v-f17dfb82>.*?</g></svg>'
    if re.search(pattern, text, flags=re.DOTALL):
        return re.sub(pattern, LETTERS_BLOCK + "</svg>", text, count=1, flags=re.DOTALL)
    return text


def patch_file(path: Path, extra: list[tuple[str, str]] | None = None) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    orig = text
    reps = CONTENT_REPS + (extra or [])
    if "sanity-assets.json" in str(path):
        reps = ASSET_REPS + reps
    for old, new in reps:
        text = text.replace(old, new)
    if path.suffix.lower() == ".html":
        text = replace_loader_letters(text)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed: list[str] = []
    targets = list(ROOT.rglob("*.html")) + list(ROOT.rglob("*.json"))
    targets += [ROOT / "sanity-assets.json"]
    skip = {"static-preview", ".git", "basis", "draco", "__pycache__"}
    for path in targets:
        if any(s in path.parts for s in skip):
            continue
        if path.name.endswith(".py"):
            continue
        if patch_file(path):
            changed.append(str(path.relative_to(ROOT)))

    # Sync public webgl copy
    src = ROOT / "webgl" / "theatre" / "main" / "state.json"
    dst = ROOT / "public" / "webgl" / "theatre" / "main" / "state.json"
    if src.exists() and dst.parent.exists():
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    print(f"Patched {len(changed)} files")


if __name__ == "__main__":
    main()
