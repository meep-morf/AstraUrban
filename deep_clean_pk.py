#!/usr/bin/env python3
"""Second-pass deep clean: slugs in payloads, cities, asset metadata."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

CITIES = {
    "karachi": {"lat": 24.8607, "lng": 67.0011, "areas": ["Clifton", "DHA Phase 6", "Defence", "Boat Basin", "Bahria Town Karachi"]},
    "lahore": {"lat": 31.5204, "lng": 74.3587, "areas": ["Gulberg", "DHA Lahore", "Model Town", "Johar Town", "MM Alam Road"]},
    "islamabad": {"lat": 33.6844, "lng": 73.0479, "areas": ["Blue Area", "F-7", "F-10", "DHA Islamabad", "Bahria Enclave"]},
    "rawalpindi": {"lat": 33.5651, "lng": 73.0169, "areas": ["Saddar", "Bahria Town Rawalpindi", "DHA Rawalpindi", "Satellite Town", "Chaklala"]},
}

SPECIAL = {
    "25-west": "astra-west", "25-south": "astra-south", "25-downtown": "astra-downtown",
    "25-estates": "astra-estates", "25-vistas": "astra-vistas",
    "breach-candy-residential": "astra-clifton-residences",
    "bandra-east-commercial-project": "astra-commercial-centre",
    "sunstream-city": "astra-stream-city",
    "sunstream-city-residential": "astra-stream-city-residential",
    "asmeeta-textile-park": "astra-industrial-park",
    "dlf-akruti-info-parks": "astra-tech-park",
}


def build_slug_map() -> dict[str, str]:
    m = dict(SPECIAL)
    for d in (ROOT / "projects").iterdir():
        if not d.is_dir():
            continue
        # reverse: new name exists, infer old from common prefixes
        pass
    # Build from known patterns in remaining content
    projects = ROOT / "projects"
    for d in projects.iterdir():
        if not d.is_dir():
            continue
        new = d.name
        if new.startswith("astra-corporate-"):
            old = new.replace("astra-corporate-", "ackruti-")
            m[old] = new
        elif new.startswith("astra-"):
            base = new[6:]
            for prefix in ("hubtown-", "akruti-", "ackruti-"):
                old = prefix + base
                if old != new:
                    m[old] = new
    return m


def coords_str(city: str, slug: str) -> str:
    base = CITIES[city]
    h = int(hashlib.md5(slug.encode()).hexdigest()[:8], 16)
    lat = base["lat"] + ((h % 1000) - 500) / 100000
    lng = base["lng"] + (((h // 1000) % 1000) - 500) / 100000
    return f"{lat:.4f} N. {lng:.4f} E"


def location_str(city: str, slug: str) -> str:
    areas = CITIES[city]["areas"]
    h = int(hashlib.md5(slug.encode()).hexdigest(), 16)
    return f"{areas[h % len(areas)]}, {city.title()}"


def slug_city(slug: str) -> str:
    h = int(hashlib.md5(slug.encode()).hexdigest(), 16)
    return ["karachi", "lahore", "islamabad", "rawalpindi"][h % 4]


def clean_text(text: str, slug_map: dict[str, str]) -> str:
    for old, new in sorted(slug_map.items(), key=lambda x: -len(x[0])):
        text = text.replace(f'"{old}"', f'"{new}"')
        text = text.replace(old, new)

    city_map = {
        '"mumbai"': '"karachi"', '"thane"': '"rawalpindi"', '"pune"': '"lahore"',
        '"gujarat"': '"lahore"', '"maharashtra"': '"sindh"', '"khalapur"': '"islamabad"',
        "Mumbai": "Karachi", "Thane": "Rawalpindi", "Pune": "Lahore", "Gujarat": "Lahore",
        "Maharashtra": "Sindh", "Vadodara": "Islamabad", "Surat": "Lahore",
        "Mehsana": "Lahore", "Andheri West": "Clifton", "Andheri East": "DHA Phase 6",
        "Mulund East": "Gulberg", "Dharavi": "Saddar", "Panch Pakhadi": "Satellite Town",
        "Vile Parle East": "Bahria Town Karachi", "Breach Candy": "Clifton",
        "Hinjewadi": "Blue Area", "Geeta Mandir": "Saddar", "Worli": "Clifton",
        "Ghatkopar": "Gulberg", "Chembur": "Defence", "Bandra": "DHA Phase 6",
        "India International Tower": "Ocean Tower Clifton",
        "DLF Astra Urban Info Parks": "Astra Tech Park",
        " Astra Urban ": " Astra Urban ",
    }
    for old, new in city_map.items():
        text = text.replace(old, new)

    # Fix coordinate patterns like 19.4 N. 72.52 E
    def repl_coord(m: re.Match) -> str:
        slug = m.group("slug") if "slug" in m.groupdict() else "default"
        city = slug_city(slug)
        return coords_str(city, slug)

    # Replace embedded lat/lng pairs in location strings
    text = re.sub(
        r'"(\d+\.?\d*)\s+N\.\s+(\d+\.?\d*)\s+E"',
        lambda m: f'"{coords_str("karachi", m.group(0))}"',
        text,
    )
    text = re.sub(r'"(\d+\.?\d*)\s+(\d+\.?\d*)"', lambda m: '"24.8607"', text)
    text = re.sub(r'"locationLatitude":"[\d.]+"', '"locationLatitude":"24.8607"', text)
    text = re.sub(r'"locationLongitude":"[\d.]+"', '"locationLongitude":"67.0011"', text)

    # Asset filename metadata
    text = re.sub(r"hubtown[_-]", "astra-", text, flags=re.I)
    text = re.sub(r"akruti[_\s-]", "astra-", text, flags=re.I)
    text = re.sub(r"ackruti[_\s-]", "astra-corporate-", text, flags=re.I)
    text = text.replace("India International", "Ocean Tower")
    text = text.replace("-mumbai-", "-karachi-")
    text = text.replace("mumbai-hubtown", "karachi-astra")

    return text


def main() -> None:
    slug_map = build_slug_map()
    # Ensure all old slugs map even if folder renamed
    extras = {
        "hubtown-celeste": "astra-celeste", "hubtown-viva": "astra-viva",
        "akruti-arcade": "astra-arcade", "dlf-akruti-info-parks": "astra-tech-park",
        "hubtown-joyos-surat": "astra-joyos-surat", "hubtown-joyos-vadodara": "astra-joyos-vadodara",
        "hubtown-joyos-geeta-mandir": "astra-joyos-geeta-mandir", "hubtown-rhythm": "astra-rhythm",
        "hubtown-skybay": "astra-skybay", "hubtown-trade-centre": "astra-trade-centre",
    }
    slug_map.update(extras)

    changed = []
    patterns = {".html", ".json", ".js", ".txt", ".webmanifest"}
    skip = {".git", "static-preview", "basis", "__pycache__", "draco"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(s in path.parts for s in skip):
            continue
        if path.suffix.lower() not in patterns and path.name not in {"PREVIEW.txt"}:
            continue
        if path.suffix.lower() == ".css":
            continue
        if path.name in {"deep_clean_pk.py", "rebrand_astra.py", "localize_pk.py"}:
            continue
        try:
            orig = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        updated = clean_text(orig, slug_map)
        if updated != orig:
            path.write_text(updated, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)))
    print(f"Deep cleaned {len(changed)} files")


if __name__ == "__main__":
    main()
