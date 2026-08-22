#!/usr/bin/env python3
"""Deep rebrand: Astra Urban Pakistan — slugs, assets, maps, logo, all content."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent

BRAND = "Astra Urban Pakistan"
BRAND_SHORT = "Astra Urban"
TAGLINE = "Shaping Pakistan's Urban Future"
DOMAIN = "astraurban.pk"
SITE_URL = "https://astra-urban-pk.vercel.app"
EMAIL = "hello@astraurban.pk"
PHONE = "+92 21 3876 4521"
WHATSAPP = "9231238764521"
ADDRESS = "Suite 1204, Ocean Tower, Clifton Block 5, Karachi 75600, Pakistan"
THEATRE = "astra-urban-pk"
DEFAULT_TITLE = f"{BRAND} | Premium Real Estate Developer"
DEFAULT_OG = (
    f"{BRAND} creates premium residential and commercial landmarks "
    "across Karachi, Lahore, Islamabad, and Rawalpindi."
)

# Nav wordmark — block ASTRA (viewBox 0 0 186 20)
NAV_LOGO_PATH = (
    "M0 0h4.043v20H0zM16.174 0h4.043v20h-4.043zM0 0h20.217v4.043H0zM4.043 8h12.131v4.043H4.043z"
    "M28.304 0h20.217v4.043H28.304zM28.304 4.043h4.043V8H28.304zM28.304 8h20.217v4.043H28.304zM"
    "44.478 12.043h4.043V15.957h-4.043zM28.304 15.957h20.217V20H28.304zM56.608 0h20.217v4.043H5"
    "6.608zM64.695 4.043h4.043V20h-4.043zM84.912 0h4.043v20H84.912zM84.912 0h16.174v4.043H84.91"
    "2zM97.043 0h4.043v12.043h-4.043zM84.912 8h16.174v4.043H84.912zM92.999 12.043h4.043V20h-4.0"
    "43zM97.043 15.957h8.086V20h-8.086zM113.216 0h4.043v20H113.216zM129.39 0h4.043v20h-4.043zM1"
    "13.216 0h20.217v4.043H113.216zM117.259 8h12.131v4.043H117.259z"
)

OLD_NAV_LOGO_PATH = (
    "M0 0h4.043v8h12.13V0h4.044v20h-4.043v-8H4.044v8H0zm28.304 0h4.044v16h12.13V0h4.044v20H28.304z"
    "M56.61 0h20.217v20H56.61zm4.043 4v4h12.13V4zm12.13 8h-12.13v4h12.13zm16.175-8H80.87V0h20.217v4H93v16h-4.043V4Zm48.521-4h4.044v16h4.043V0h4.044v16h4.043V0h4.044v20h-20.218zm28.305 0H186v20h-4.043V4h-12.131v16h-4.043V0ZM129.39 20h-20.218V0h20.218zm-4.042-4V4h-12.131z"
)

SKIP_DIRS = {"__pycache__", "node_modules", ".git", "basis", "draco"}
NEVER_TOUCH_SUFFIXES = {".css", ".scss", ".pyc", ".png", ".jpg", ".jpeg", ".webp", ".woff", ".woff2", ".otf", ".ttf", ".ico", ".wasm", ".bin", ".tif", ".mhtml"}

CITIES = {
    "karachi": {"lat": 24.8607, "lng": 67.0011, "areas": ["Clifton", "DHA Phase 6", "Defence", "Boat Basin", "Bahria Town Karachi"]},
    "lahore": {"lat": 31.5204, "lng": 74.3587, "areas": ["Gulberg", "DHA Lahore", "Model Town", "Johar Town", "MM Alam Road"]},
    "islamabad": {"lat": 33.6844, "lng": 73.0479, "areas": ["Blue Area", "F-7", "F-10", "DHA Islamabad", "Bahria Enclave"]},
    "rawalpindi": {"lat": 33.5651, "lng": 73.0169, "areas": ["Saddar", "Bahria Town Rawalpindi", "DHA Rawalpindi", "Satellite Town", "Chaklala"]},
}

SPECIAL_SLUGS = {
    "25-west": "astra-west",
    "25-south": "astra-south",
    "25-downtown": "astra-downtown",
    "25-estates": "astra-estates",
    "25-vistas": "astra-vistas",
    "breach-candy-residential": "astra-clifton-residences",
    "bandra-east-commercial-project": "astra-commercial-centre",
    "sunstream-city": "astra-stream-city",
    "sunstream-city-residential": "astra-stream-city-residential",
    "asmeeta-textile-park": "astra-industrial-park",
    "dlf-akruti-info-parks": "astra-tech-park",
}

SPECIAL_TITLES = {
    "astra-west": "Astra West",
    "astra-south": "Astra South",
    "astra-downtown": "Astra Downtown",
    "astra-estates": "Astra Estates",
    "astra-vistas": "Astra Vistas",
    "astra-clifton-residences": "Astra Clifton Residences",
    "astra-commercial-centre": "Astra Commercial Centre",
    "astra-stream-city": "Astra Stream City",
    "astra-stream-city-residential": "Astra Stream City Residences",
    "astra-industrial-park": "Astra Industrial Park",
    "astra-tech-park": "Astra Tech Park",
}


def build_slug_map() -> dict[str, str]:
    mapping: dict[str, str] = dict(SPECIAL_SLUGS)
    projects = ROOT / "projects"
    if not projects.is_dir():
        return mapping
    for d in sorted(projects.iterdir()):
        if not d.is_dir():
            continue
        old = d.name
        if old in mapping:
            continue
        if old.startswith("hubtown-"):
            mapping[old] = old.replace("hubtown-", "astra-")
        elif old.startswith("akruti-"):
            mapping[old] = old.replace("akruti-", "astra-")
        elif old.startswith("ackruti-"):
            mapping[old] = old.replace("ackruti-", "astra-corporate-")
    return mapping


def slug_to_title(slug: str) -> str:
    if slug in SPECIAL_TITLES:
        return SPECIAL_TITLES[slug]
    base = slug
    for prefix in ("astra-corporate-", "astra-", "hubtown-", "akruti-", "ackruti-"):
        if base.startswith(prefix):
            base = base[len(prefix) :]
            break
    return f"Astra {base.replace('-', ' ').title()}".strip()


def slug_to_city(slug: str) -> str:
    h = int(hashlib.md5(slug.encode()).hexdigest(), 16)
    pool = ["karachi", "lahore", "islamabad", "rawalpindi"]
    return pool[h % 4]


def content_replacements(slug_map: dict[str, str]) -> list[tuple[str, str]]:
    reps: list[tuple[str, str]] = [
        ("Meridian Developments Pakistan", BRAND),
        ("Meridian Developments", BRAND),
        ("About Meridian", f"About {BRAND_SHORT}"),
        ("Contact Meridian", f"Contact {BRAND_SHORT}"),
        ("Meridian Careers", f"{BRAND_SHORT} Careers"),
        ("Meridian News", f"{BRAND_SHORT} News"),
        ("Meridian Residences", f"{BRAND_SHORT} Residences"),
        ("Meridian creates", f"{BRAND_SHORT} creates"),
        ("At Meridian we", f"At {BRAND_SHORT} we"),
        ("At Meridian ", f"At {BRAND_SHORT} "),
        (" the Meridian vision", f" the {BRAND_SHORT} vision"),
        ("© 2026 Meridian Developments Pakistan", f"© 2026 {BRAND}"),
        ("© 2026 Meridian", f"© 2026 {BRAND}"),
        ("Meridian ", f"{BRAND_SHORT} "),
        (" Meridian", f" {BRAND_SHORT}"),
        ("Meridian", BRAND_SHORT),
        ("meridian-pk.vercel.app", SITE_URL.replace("https://", "")),
        ("https://meridian-pk.vercel.app", SITE_URL),
        ("meridian-pk", THEATRE),
        ("meridiandevelopments.pk", DOMAIN),
        ("hello@meridiandevelopments.pk", EMAIL),
        ("meridian-developments-pakistan", "astra-urban-pakistan"),
        ("meridiandevelopments.pk", DOMAIN),
        ("Hubtown Limited", BRAND),
        ("About Hubtown", f"About {BRAND_SHORT}"),
        ("Hubtown ", f"{BRAND_SHORT} "),
        (" Hubtown", f" {BRAND_SHORT}"),
        ("Hubtown", BRAND_SHORT),
        ("hubtown.co.in", DOMAIN),
        ("https://hubtown-live.netlify.app", SITE_URL),
        ("http://hubtown-live.netlify.app", SITE_URL),
        ("hubtown-live", THEATRE),
        ('theatreProjectName:"hubtown"', f'theatreProjectName:"{THEATRE}"'),
        ('theatreProjectName:"meridian-pk"', f'theatreProjectName:"{THEATRE}"'),
        ('name:"hubtown-live"', f'name:"{THEATRE}"'),
        ('name:"meridian-pk"', f'name:"{THEATRE}"'),
        ("linkedin.com/company/hubtown", "linkedin.com/company/astra-urban-pakistan"),
        ("instagram.com/hubtown", "instagram.com/astraurban.pk"),
        ("facebook.com/hubtown", "facebook.com/astraurbanpk"),
        ("Central Suburbs", "Islamabad"),
        ("South Mumbai", "Karachi"),
        ("Western Suburbs", "Lahore"),
        ("<!--[-->Thane<!--]-->", "<!--[-->Rawalpindi<!--]-->"),
        (">Thane<", ">Rawalpindi<"),
        ("Ackruti City", BRAND_SHORT),
        ("Ackruti", BRAND_SHORT),
        ("Akruti", BRAND_SHORT),
        ("India's", "Pakistan's"),
        ("India's", "Pakistan's"),
        (" in India", " in Pakistan"),
        ("India & Mumbai", "Pakistan"),
        ("Mumbai & India", "Pakistan"),
        ("Mumbai Metropolitan Region", "Karachi, Lahore, Islamabad and Rawalpindi"),
        ("Mumbai Suburban", "Karachi"),
        ("Maharashtra", "Sindh"),
        ("Mumbai", "Karachi"),
        ("Indian", "Pakistani"),
        (" India", " Pakistan"),
        ("en-IN", "en-PK"),
        ('addressCountry IN', 'addressCountry PK'),
        ("₹", "Rs."),
        ("INR", "PKR"),
        ("+91", "+92"),
        ("info@hubtown.co.in", EMAIL),
        ("sales@hubtown.co.in", EMAIL),
        ("8657995844", WHATSAPP[3:]),
        ("918657995844", WHATSAPP),
        ("wa.me/918657995844", f"wa.me/{WHATSAPP}"),
        ("https://wa.me/918657995844", f"https://wa.me/{WHATSAPP}"),
        (OLD_NAV_LOGO_PATH, NAV_LOGO_PATH),
    ]
    # Slug replacements longest first
    for old, new in sorted(slug_map.items(), key=lambda x: -len(x[0])):
        reps.append((f"/projects/{old}", f"/projects/{new}"))
        reps.append((f"/projects/{old}/", f"/projects/{new}/"))
        reps.append((f'"slug":"{old}"', f'"slug":"{new}"'))
        reps.append((f'"slug": "{old}"', f'"slug": "{new}"'))
        new_title = slug_to_title(new)
        if old.startswith("hubtown-"):
            base = old.replace("hubtown-", "").replace("-", " ").title()
            reps.append((f"Hubtown {base}", new_title))
            reps.append((f"Meridian {base}", new_title))
        if old.startswith("akruti-") or old.startswith("ackruti-"):
            base = re.sub(r"^(akruti|ackruti)-", "", old).replace("-", " ").title()
            reps.append((f"Akruti {base}", new_title))
            reps.append((f"Ackruti {base}", new_title))
            reps.append((f"Meridian {base}", new_title))
    return reps


def apply_replacements(text: str, reps: list[tuple[str, str]]) -> str:
    for old, new in reps:
        text = text.replace(old, new)
    return text


def rename_project_folders(slug_map: dict[str, str]) -> list[str]:
    renamed = []
    projects = ROOT / "projects"
    for old, new in sorted(slug_map.items(), key=lambda x: -len(x[0])):
        src = projects / old
        dst = projects / new
        if src.is_dir() and not dst.exists():
            src.rename(dst)
            renamed.append(f"{old} -> {new}")
    return renamed


def patch_site_webmanifest(text: str) -> str:
    data = json.loads(text)
    data["name"] = BRAND_SHORT
    data["short_name"] = "Astra"
    return json.dumps(data, indent=2) + "\n"


def patch_static_preview_content(text: str) -> str:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return text
    data["title"] = DEFAULT_TITLE
    if "bodyText" in data:
        data["bodyText"] = data["bodyText"].replace("Meridian Developments Pakistan", BRAND)
        data["bodyText"] = data["bodyText"].replace("Meridian creates", f"{BRAND_SHORT} creates")
    return json.dumps(data, indent=2) + "\n"


def download_share_asset() -> bool:
    url = "https://images.unsplash.com/photo-1582555172862-f73f8156545c?w=1200&h=630&fit=crop&q=80"
    dest = ROOT / "images" / "share_asset.jpg"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=60).read()
        dest.write_bytes(data)
        return True
    except OSError as e:
        print(f"Warning: could not download share_asset.jpg: {e}")
        return False


def sync_webgl_copies() -> None:
    src = ROOT / "webgl" / "theatre" / "main" / "state.json"
    dst = ROOT / "public" / "webgl" / "theatre" / "main" / "state.json"
    if src.exists() and dst.parent.exists():
        shutil.copy2(src, dst)


def should_process(path: Path) -> bool:
    if any(p in path.parts for p in SKIP_DIRS):
        return False
    if path.name in {"rebrand_astra.py", "localize_pk.py"}:
        return False
    if path.suffix.lower() in NEVER_TOUCH_SUFFIXES and path.name != "site.webmanifest":
        return False
    return True


def process_files(reps: list[tuple[str, str]]) -> list[str]:
    changed = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or not should_process(path):
            continue
        suffix = path.suffix.lower()
        if suffix not in {".html", ".json", ".js", ".txt", ".webmanifest", ".py"} and path.name not in {
            "PREVIEW.txt",
        }:
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        if path.name == "site.webmanifest":
            updated = patch_site_webmanifest(original)
        elif path.name == "content.json" and "static-preview" in path.parts:
            updated = patch_static_preview_content(original)
        elif path.name == "PREVIEW.txt":
            updated = (
                f"{BRAND} — localized preview\n"
                f"{'=' * len(BRAND)}\n\n"
                f"Brand: {BRAND}\n"
                f"Tagline: {TAGLINE}\n"
                f"Domain: {DOMAIN} (deploy: {SITE_URL})\n\n"
                "Original template: Hubtown India clone (fully rebranded for Pakistan)\n\n"
                "Preview server:\n"
                "  python serve_proxy.py\n"
                "  Then open: http://127.0.0.1:8765/\n"
            )
        else:
            updated = apply_replacements(original, reps)

        updated = updated.replace('lang="en"', 'lang="en-PK"')
        updated = re.sub(r'"locationLatitude":\s*"[\d.]+"', '"locationLatitude":"24.8607"', updated)
        updated = re.sub(r'"locationLongitude":\s*"[\d.]+"', '"locationLongitude":"67.0011"', updated)

        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)))
    return changed


def update_localize_pk() -> None:
    path = ROOT / "localize_pk.py"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    text = text.replace('"""Safe content-only localization for Meridian Developments Pakistan."""',
                        f'"""Safe content-only localization for {BRAND}."""')
    text = re.sub(r'BRAND = ".*?"', f'BRAND = "{BRAND}"', text)
    text = re.sub(r'BRAND_SHORT = ".*?"', f'BRAND_SHORT = "{BRAND_SHORT}"', text)
    text = re.sub(r'DOMAIN = ".*?"', f'DOMAIN = "{DOMAIN}"', text)
    text = re.sub(r'SITE_URL = ".*?"', f'SITE_URL = "{SITE_URL}"', text)
    text = re.sub(r'EMAIL = ".*?"', f'EMAIL = "{EMAIL}"', text)
    text = text.replace("Meridian West", "Astra West")
    text = text.replace("Meridian ", "Astra ")
    text = text.replace('"meridian-pk"', f'"{THEATRE}"')
    text = text.replace("meridian-pk", THEATRE)
    path.write_text(text, encoding="utf-8")


def write_slug_redirects(slug_map: dict[str, str]) -> None:
    """Inject redirect map into serve_proxy.py if not present."""
    path = ROOT / "serve_proxy.py"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    block = "SLUG_REDIRECTS = {\n"
    for old, new in sorted(slug_map.items()):
        block += f'    "/projects/{old}": "/projects/{new}",\n'
        block += f'    "/projects/{old}/": "/projects/{new}/",\n'
    block += "}\n\n"
    if "SLUG_REDIRECTS" not in text:
        text = text.replace("PORT = 8765\n", f"PORT = 8765\n\n{block}")
        marker = "        parsed = urlparse(self.path)\n"
        inject = (
            "        parsed = urlparse(self.path)\n"
            "        redirect = SLUG_REDIRECTS.get(parsed.path)\n"
            "        if redirect:\n"
            "            self.send_response(301)\n"
            "            self.send_header('Location', redirect)\n"
            "            self.end_headers()\n"
            "            return\n"
        )
        text = text.replace(marker, inject)
        text = text.replace("ORIGIN_HOST = \"hubtown.co.in\"", f"ORIGIN_HOST = \"{DOMAIN}\"")
        text = text.replace("HubtownLocalClone", "AstraUrbanClone")
        text = text.replace("Hubtown clone", f"{BRAND_SHORT} clone")
        path.write_text(text, encoding="utf-8")


def main() -> None:
    slug_map = build_slug_map()
    print(f"Slug map: {len(slug_map)} projects")

    renamed = rename_project_folders(slug_map)
    print(f"Renamed {len(renamed)} project folders")

    reps = content_replacements(slug_map)
    changed = process_files(reps)
    print(f"Updated {len(changed)} files")

    update_localize_pk()
    write_slug_redirects(slug_map)
    sync_webgl_copies()
    downloaded = download_share_asset()
    print(f"Share asset downloaded: {downloaded}")

    # Mark static-preview deprecated note
    note = ROOT / "static-preview" / "DEPRECATED.txt"
    note.write_text(
        "This folder is a legacy capture from the original Hubtown template.\n"
        f"Use the live clone at http://127.0.0.1:8765/ for {BRAND} preview.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
