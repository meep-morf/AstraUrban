#!/usr/bin/env python3
"""Remove AudioPrompt overlay from minified Nuxt bundle."""
from pathlib import Path

BUNDLE = Path("_nuxt/u1ipQrxM.js")

OLD_WATCHERS = (
    "return zn(()=>{}),an(r,()=>{}),Gs(()=>{window.removeEventListener"
)
NEW_WATCHERS = (
    "return Gs(()=>{window.removeEventListener"
)

OLD_RENDER_PREFIX = "(P,S)=>{const E=Ui;return K(s)?"
NEW_RENDER = "(P,S)=>Vt('',!0)"

def main() -> None:
    text = BUNDLE.read_text(encoding="utf-8")

    if NEW_RENDER in text and OLD_WATCHERS not in text:
        print("AudioPrompt already patched")
        return

    if OLD_RENDER_PREFIX not in text:
        raise SystemExit("AudioPrompt render prefix not found")

    start = text.index(OLD_RENDER_PREFIX)
    end_marker = "}),mbe=Object.assign(pbe,{__name:\"AudioPrompt\"})"
    end = text.index(end_marker, start)
    old_render = text[start:end]

    updated = text[:start] + NEW_RENDER + text[end:]

    if OLD_WATCHERS in updated:
        updated = updated.replace(OLD_WATCHERS, NEW_WATCHERS, 1)

    BUNDLE.write_text(updated, encoding="utf-8")
    print(f"Patched AudioPrompt: removed {len(old_render)} chars of render logic")

if __name__ == "__main__":
    main()
