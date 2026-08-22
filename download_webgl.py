#!/usr/bin/env python3
"""Download Hubtown WebGL assets required for the homepage experience."""
from __future__ import annotations

import re
import ssl
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://hubtown.co.in"
OUT = Path(r"D:\real estate\hubtown-clone")
CTX = ssl.create_default_context()
UA = {"User-Agent": "Mozilla/5.0"}

ASSETS = [
    "/webgl/theatre/main/state.json",
    "/public/webgl/theatre/main/state.json",
    "/webgl/data/scene3_pts_background.json",
    "/webgl/data/scene3_pts_foreground.json",
    "/webgl/data/scene4_cubes.json",
    "/webgl/models/map-cube.glb",
    "/webgl/models/map-districts.glb",
    "/webgl/models/map.glb",
    "/webgl/models/scene_1.glb",
    "/webgl/models/scene_2-line.glb",
    "/webgl/models/scene_2.glb",
    "/webgl/models/scene_3.glb",
    "/webgl/models/scene_4.glb",
    "/webgl/textures/28.png",
    "/webgl/textures/cubeThicknessMap.png",
    "/webgl/textures/cubeThicknessMapBase.png",
    "/webgl/textures/hero-cube-ao.png",
    "/webgl/textures/hero-cube-details.jpg",
    "/webgl/textures/hero-cube-edges.png",
    "/webgl/textures/hero-cube-grid.png",
    "/webgl/textures/hero-cube-hex.png",
    "/webgl/textures/map_coast_mask.png",
    "/webgl/textures/map_terrain_normal.png",
    "/webgl/textures/matcap.png",
    "/webgl/textures/matcap2.jpg",
    "/webgl/textures/noise_1.jpg",
    "/webgl/textures/noise_2.png",
    "/webgl/textures/scene2_terrain_Normal.jpg",
    "/webgl/textures/scene3-houdini-height.exr",
    "/webgl/textures/scene3_terrain_Normal.png",
    "/webgl/textures/scene4-houdini-height.exr",
    "/webgl/textures/square-displacement.png",
    "/webgl/textures/voronoi.png",
    "/webgl/textures/water-normal.jpg",
    # ktx2 variants under public/
    "/public/webgl/textures/28.ktx2",
    "/public/webgl/textures/cubeThicknessMap.ktx2",
    "/public/webgl/textures/cubeThicknessMapBase.ktx2",
    "/public/webgl/textures/hero-cube-ao.ktx2",
    "/public/webgl/textures/hero-cube-details.ktx2",
    "/public/webgl/textures/hero-cube-edges.ktx2",
    "/public/webgl/textures/hero-cube-grid.ktx2",
    "/public/webgl/textures/hero-cube-hex.ktx2",
    "/public/webgl/textures/map_terrain_normal.ktx2",
    "/public/webgl/textures/matcap.ktx2",
    "/public/webgl/textures/matcap2.ktx2",
    "/public/webgl/textures/noise_1.ktx2",
    "/public/webgl/textures/noise_2.ktx2",
    "/public/webgl/textures/scene2_terrain_Normal.ktx2",
    "/public/webgl/textures/scene3_terrain_Normal.ktx2",
    "/public/webgl/textures/square-displacement.ktx2",
    "/public/webgl/textures/terrain_normal.ktx2",
    "/public/webgl/textures/voronoi.ktx2",
    "/public/webgl/textures/water-normal.ktx2",
]


def fetch(url: str) -> bytes:
    last = None
    for i in range(3):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, context=CTX, timeout=180) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1 + i)
    raise RuntimeError(str(last))


def main() -> None:
    ok = 0
    for rel in ASSETS:
        dest = OUT / rel.lstrip("/")
        if dest.exists() and dest.stat().st_size > 0:
            print("skip", rel)
            ok += 1
            continue
        try:
            data = fetch(BASE + rel)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            print("OK", rel, len(data))
            ok += 1
        except Exception as e:  # noqa: BLE001
            print("FAIL", rel, e)

    # Also scrape more paths from downloaded state.json if present
    for state in [
        OUT / "webgl/theatre/main/state.json",
        OUT / "public/webgl/theatre/main/state.json",
    ]:
        if not state.exists():
            continue
        text = state.read_text(encoding="utf-8", errors="ignore")
        extra = set(re.findall(r'["\'](/?(?:public/)?webgl/[^"\']+)["\']', text))
        for rel in sorted(extra):
            if not rel.startswith("/"):
                rel = "/" + rel
            dest = OUT / rel.lstrip("/")
            if dest.exists():
                continue
            try:
                data = fetch(BASE + rel)
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
                print("EXTRA", rel, len(data))
            except Exception as e:  # noqa: BLE001
                print("EXTRA FAIL", rel, e)

    print("done, successful-ish", ok)


if __name__ == "__main__":
    main()
