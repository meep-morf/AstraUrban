#!/usr/bin/env python3
"""Capture comparison screenshots of original vs local Astra Urban clone."""
from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(r"D:\real estate\hubtown-clone\previews")
OUT.mkdir(parents=True, exist_ok=True)

TARGETS = [
    ("original", "https://astraurban.pk/"),
    ("clone", "http://127.0.0.1:8765/"),
]


def capture(page, name: str, url: str) -> dict:
    console: list[dict] = []
    failed: list[dict] = []

    page.on("console", lambda msg: console.append({"type": msg.type, "text": msg.text}))
    page.on(
        "requestfailed",
        lambda req: failed.append({"url": req.url, "failure": req.failure}),
    )

    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto(url, wait_until="networkidle", timeout=120_000)
    page.wait_for_timeout(15000)
    # Dismiss loader if still visible by waiting for hero text
    try:
        page.wait_for_selector("text=We build", timeout=30_000)
    except Exception:
        pass
    page.wait_for_timeout(3000)

    shot = OUT / f"{name}-homepage.png"
    page.screenshot(path=str(shot), full_page=False)
    title = page.title()
    hero = page.locator("text=We build").first.is_visible()
    return {
        "url": url,
        "screenshot": str(shot),
        "title": title,
        "hero_visible": hero,
        "console_errors": [c for c in console if c["type"] == "error"][:10],
        "failed_requests": failed[:10],
    }


def main() -> None:
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--use-gl=angle",
                "--enable-webgl",
                "--ignore-gpu-blocklist",
            ],
        )
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=1,
        )
        for name, url in TARGETS:
            page = context.new_page()
            print(f"Capturing {name} ...")
            try:
                info = capture(page, name, url)
                results.append({"name": name, **info})
                print(f"  saved {info['screenshot']} hero={info['hero_visible']}")
            except Exception as e:  # noqa: BLE001
                results.append({"name": name, "url": url, "error": str(e)})
                print(f"  ERROR {e}")
            page.close()
        browser.close()

    report = OUT / "comparison.json"
    report.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Report: {report}")


if __name__ == "__main__":
    main()
