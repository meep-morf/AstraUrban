#!/usr/bin/env python3
"""Safe content-only localization for Astra Urban Pakistan."""
from __future__ import annotations

import hashlib
import re
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

DEFAULT_TITLE = f"{BRAND} | Premium Real Estate Developer"
DEFAULT_OG = (
    f"{BRAND} creates premium residential and commercial landmarks "
    "across Karachi, Lahore, Islamabad, and Rawalpindi."
)

CITIES = {
    "karachi": {"lat": 24.8607, "lng": 67.0011, "areas": ["Clifton", "DHA Phase 6", "Defence", "Boat Basin", "Bahria Town Karachi"]},
    "lahore": {"lat": 31.5204, "lng": 74.3587, "areas": ["Gulberg", "DHA Lahore", "Model Town", "Johar Town", "MM Alam Road"]},
    "islamabad": {"lat": 33.6844, "lng": 73.0479, "areas": ["Blue Area", "F-7", "F-10", "DHA Islamabad", "Bahria Enclave"]},
    "rawalpindi": {"lat": 33.5651, "lng": 73.0169, "areas": ["Saddar", "Bahria Town Rawalpindi", "DHA Rawalpindi", "Satellite Town", "Chaklala"]},
}

SKIP_DIRS = {"__pycache__", "node_modules", ".git", "basis", "draco"}
NEVER_TOUCH_SUFFIXES = {".css", ".scss", ".py", ".pyc", ".png", ".jpg", ".jpeg", ".webp", ".woff", ".woff2", ".otf", ".ttf", ".ico", ".wasm", ".bin", ".tif", ".mhtml"}

JS_SAFE_REPLACEMENTS = [
    ("Central Suburbs", "Islamabad"),
    ("South Mumbai", "Karachi"),
    ("Western Suburbs", "Lahore"),
    ("Hubtown Limited", BRAND),
    ("About Hubtown", f"About {BRAND_SHORT}"),
    ("Hubtown ", f"{BRAND_SHORT} "),
    (" Hubtown", f" {BRAND_SHORT}"),
    ("Hubtown", BRAND_SHORT),
    ("hubtown.co.in", DOMAIN),
    ("https://hubtown-live.netlify.app", SITE_URL),
    ("8657995844", WHATSAPP[3:]),
    ("918657995844", WHATSAPP),
    ("wa.me/918657995844", f"wa.me/{WHATSAPP}"),
    ("+91", "+92"),
    ("info@hubtown.co.in", EMAIL),
    ("sales@hubtown.co.in", EMAIL),
    ("in India", "in Pakistan"),
    ("India & Mumbai", "Pakistan"),
    ("Mumbai & India", "Pakistan"),
    ("Real Estate Developer in India", "Real Estate Developer in Pakistan"),
    ("Leading Real Estate Developer in India", "Premium Real Estate Developer in Pakistan"),
    ("theatreProjectName:\"hubtown\"", 'theatreProjectName:"astra-urban-pk"'),
    ('name:"hubtown-live"', 'name:"astra-urban-pk"'),
    ("linkedin.com/company/hubtown", "linkedin.com/company/meridian-developments-pakistan"),
    ("instagram.com/hubtown", "instagram.com/meridiandevelopments.pk"),
    ("facebook.com/hubtown", "facebook.com/meridiandevelopmentspk"),
]

CONTENT_REPLACEMENTS = [
    (
        "Hubtown Limited (formerly known as Ackruti City Limited) is one of India’s leading real estate developers, with over four decades of experience developing residential and commercial spaces and IT parks across India. The company primarily focuses on the Mumbai Metropolitan Region, Pune, and Gujarat. Hubtown has successfully delivered over 45 million sq. ft. of real estate, with an additional 20 million sq. ft. currently under development and 10 million sq. ft. planned for upcoming projects.",
        DEFAULT_OG,
    ),
    (
        "Hubtown Limited (formerly known as Ackruti City Limited) is one of India's leading real estate developers, with over four decades of experience developing residential and commercial spaces and IT parks across India. The company primarily focuses on the Mumbai Metropolitan Region, Pune, and Gujarat. Hubtown has successfully delivered over 45 million sq. ft. of real estate, with an additional 20 million sq. ft. currently under development and 10 million sq. ft. planned for upcoming projects.",
        DEFAULT_OG,
    ),
    ("Hubtown Limited | Leading Real Estate Developer in India", DEFAULT_TITLE),
    ("About Hubtown | Leading Real Estate Developer in Mumbai & India", f"About {BRAND_SHORT} | Premium Developer in Pakistan"),
    ("Contact Hubtown Limited | Real Estate Developer in India", f"Contact {BRAND} | Real Estate Developer in Pakistan"),
    ("Hubtown Careers | Real Estate Jobs in India & Mumbai", f"{BRAND_SHORT} Careers | Real Estate Jobs in Pakistan"),
    ("Hubtown News & Updates | Real Estate Developer India", f"{BRAND_SHORT} News & Updates | Real Estate Developer Pakistan"),
    (
        "Learn about Hubtown, a leading real estate developer in Mumbai and India with expertise in residential, commercial and redevelopment projects across key locations.",
        f"Learn about {BRAND_SHORT}, a premium real estate developer in Pakistan with expertise in residential, commercial and mixed-use projects across major cities.",
    ),
    (
        "Get in touch with Hubtown Limited, a trusted real estate developer in India. Contact us for residential and commercial projects, sales enquiries or support.",
        f"Get in touch with {BRAND}. Contact us for residential and commercial projects, sales enquiries or support across Pakistan.",
    ),
    (
        "Explore career opportunities at Hubtown Limited. Join a leading real estate developer in India and build your future across residential and commercial projects.",
        f"Explore career opportunities at {BRAND}. Join a premium Pakistani developer and build your future across residential and commercial projects.",
    ),
    (
        "Stay updated with the latest news, announcements and developments from Hubtown Limited, a trusted real estate developer in India.",
        f"Stay updated with the latest news and announcements from {BRAND}.",
    ),
    (
        "For over 40 years, Hubtown has created some of India’s most innovative real estate developments, spanning across Residential, Commercial and Industrial projects. From the drawing board to reality, across all facets of society.",
        f"{BRAND_SHORT} creates thoughtful residential, commercial and mixed-use developments across Pakistan — from concept to completion, for communities that endure.",
    ),
    (
        "For over 40 years, Hubtown has created some of India' most innovative real estate developments, spanning across Residential, Commercial and Industrial projects. From the drawing board to reality, across all facets of society. ",
        f"{BRAND_SHORT} creates thoughtful residential, commercial and mixed-use developments across Pakistan — from concept to completion, for communities that endure. ",
    ),
    (
        "For over 40 years, Hubtown has created some of India's most innovative real estate developments, spanning across Residential, Commercial and Industrial projects. From the drawing board to reality, across all facets of society.",
        f"{BRAND_SHORT} creates thoughtful residential, commercial and mixed-use developments across Pakistan — from concept to completion, for communities that endure.",
    ),
    (
        "We build <br class=\"sm:hidden\"> the future <br> of real estate",
        "We shape <br class=\"sm:hidden\"> the future <br> of Pakistan's cities",
    ),
    (
        "WE BUILD THE FUTURE\nOF REAL ESTATE",
        "WE SHAPE THE FUTURE\nOF PAKISTAN'S CITIES",
    ),
    (
        "At Hubtown we look at the world through a different lens; instead of seeing what is, we see what could be. Each day we seek better ways to design, build and create communities.",
        f"At {BRAND_SHORT} we look at Pakistan's cities through a different lens — seeing what could be, not only what is. Each day we seek better ways to design, build and shape communities.",
    ),
    (
        "Revered as one of the most reliable Real Estate developers in India",
        "A trusted name in premium Pakistani real estate",
    ),
    (
        "Formerly known as Ackruti City Limited, Hubtown is one of India’s leading real estate companies, with over 4 decades of experience, with projects covering the entire spectrum of real estate development including Residential, Commercial, IT, Industrial, Infrastructure.",
        f"{BRAND} develops residential, commercial and mixed-use projects across Pakistan's major urban centres.",
    ),
    (
        "Being an Industry Leader our vision is to be the creator of value and enduring experiences for customers and our partners, to build remarkable landmarks that resonate our brand values.",
        "Our vision is to create enduring value and remarkable landmarks that reflect our commitment to quality, design and community.",
    ),
    (
        "Hubtown is guided by core values of teamwork, innovation, consistency, and transparency. The company leverages collective talent to drive productivity, enhances lifestyles through engineering expertise and forward-thinking design, maintains quality standards across all processes, and ensures open communication with all stakeholders.",
        f"{BRAND_SHORT} is guided by teamwork, innovation, consistency and transparency — delivering quality developments with open communication at every stage.",
    ),
    ("Contact us to learn about the Hubtown vision", f"Contact us to learn about the {BRAND_SHORT} vision"),
    ("About Hubtown", f"About {BRAND_SHORT}"),
    (
        "HUBTOWN SEASONS, CTS No. 469-A, OPP. JAIN TEMPLE, R.K. CHEMBURKAR MARG, CHEMBUR EAST, Mumbai Suburban,\nMaharashtra, 400071",
        ADDRESS,
    ),
    ("https://wa.me/918657995844", f"https://wa.me/{WHATSAPP}"),
    ("hubtown.co.in", DOMAIN),
    ("https://hubtown-live.netlify.app", SITE_URL),
    ("http://hubtown-live.netlify.app", SITE_URL),
    ("hubtown-live", "astra-urban-pk"),
    ("Central Suburbs", "Islamabad"),
    ("South Mumbai", "Karachi"),
    ("Western Suburbs", "Lahore"),
    ("Ackruti City", BRAND_SHORT),
    ("Ackruti", BRAND_SHORT),
    ("Akruti", BRAND_SHORT),
    ("Hubtown Limited", BRAND),
    ("Hubtown ", f"{BRAND_SHORT} "),
    (" Hubtown", f" {BRAND_SHORT}"),
    ("Hubtown", BRAND_SHORT),
    ("India’s", "Pakistan's"),
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
    ("Rajeevan Paramban", "Operations Team Member"),
    ("Laxmikant K. Mukhedkar", "Project Team Member"),
    ("Madhavi Degaonkar", "Corporate Team Member"),
    ("Executive Vice President Operations", "Operations Leadership"),
    ("Manager Operations", "Project Operations"),
    ("Senior Manager Company Secretary", "Corporate Services"),
    ("Hemant M Shah", ""),
    ("Originally Named", "Focus"),
    ("Chairman", "Leadership"),
    ("Founded in 1989", "Pakistan-wide portfolio"),
    ("550+ Employees", "Multidisciplinary teams"),
    ("45 million square feet", "premium developments"),
    ("20 million square feet", "active pipeline"),
    ("10 million square feet", "future pipeline"),
    ("Delivered across Commercial, Residential, and mixed-use projects.", "Delivered across commercial, residential and mixed-use projects."),
    ("Under construction in urban and suburban areas.", "Currently under development across key Pakistani cities."),
    ("Planned for future developments and expansions.", "Planned for future expansion across Pakistan."),
    ("Shaping Mumbai’s Next Residential Chapters: Hubtown Unveils Celeste in Worli and Rising City in Ghatkopar", f"{BRAND_SHORT} unveils new residential landmarks in Karachi and Lahore"),
    ("Shaping Mumbai's Next Residential Chapters: Hubtown Unveils Celeste in Worli and Rising City in Ghatkopar", f"{BRAND_SHORT} unveils new residential landmarks in Karachi and Lahore"),
    ("Celebrating milestones in Mumbai's luxury real estate", "Celebrating milestones in Pakistan's premium real estate"),
    ("Harnaaz attends Mumbai's Luxury Real Estate Awards", "Industry recognition for premium Pakistani developments"),
    ("Times Real Estate Conclave Awards 2025 - 2026, powered by Bombay Times", "Pakistan Real Estate Excellence Forum"),
    ("Times of India - Special Supplement for Gudi Padwa", "Dawn Property Supplement"),
    ("25 Residences wins the Iconic Luxury Landmark Award for 25 Downtown, Mahalaxmi ", f"{BRAND_SHORT} Residences recognised for urban design excellence"),
    ("Luxury Real Estate with a touch of Bollywood Aesthetic", "Premium living with contemporary Pakistani design"),
    ("Grand platform to recognise Real Estate excellence", "A platform celebrating real estate excellence in Pakistan"),
    ("discover our vision", "Discover our vision"),
    ("explore our projects", "Explore our projects"),
    ("© 2025 Hubtown", f"© 2026 {BRAND}"),
    ("© 2024 Hubtown", f"© 2026 {BRAND}"),
    ("© Hubtown", f"© 2026 {BRAND}"),
    ("8657995844", WHATSAPP[3:]),
    ("918657995844", WHATSAPP),
    ("+91", "+92"),
    ("info@hubtown.co.in", EMAIL),
]


def slug_to_city(slug: str, old_city: str = "") -> str:
    h = int(hashlib.md5(slug.encode()).hexdigest(), 16)
    old = (old_city or "").lower()
    if old == "mumbai":
        return "karachi"
    if old == "thane":
        return "rawalpindi"
    if old in ("pune", "gujarat", "khalapur", "maharashtra"):
        return "lahore" if h % 2 else "islamabad"
    pool = ["karachi", "lahore", "islamabad", "rawalpindi"]
    return pool[h % 4]


def coords_str(city: str, slug: str) -> str:
    base = CITIES[city]
    h = int(hashlib.md5(slug.encode()).hexdigest()[:8], 16)
    lat = base["lat"] + ((h % 1000) - 500) / 100000
    lng = base["lng"] + (((h // 1000) % 1000) - 500) / 100000
    return f"{lat:.4f} N. {lng:.4f} E"


def location_str(city: str, slug: str) -> str:
    areas = CITIES[city]["areas"]
    h = int(hashlib.md5(slug.encode()).hexdigest(), 16)
    area = areas[h % len(areas)]
    return f"{area}, {city.title()}"


def slug_to_title(slug: str) -> str:
    slug = slug.strip().lower()
    special = {
        "25-west": "Astra West",
        "25-south": "Astra South",
        "25-downtown": "Astra Downtown",
        "25-estates": "Astra Estates",
        "25-vistas": "Astra Vistas",
        "breach-candy-residential": "Astra Clifton Residences",
        "bandra-east-commercial-project": "Astra Commercial Centre",
        "sunstream-city": "Astra Stream City",
        "sunstream-city-residential": "Astra Stream City",
        "asmeeta-textile-park": "Astra Industrial Park",
        "dlf-akruti-info-parks": "Astra Tech Park",
    }
    if slug in special:
        return special[slug]
    parts = slug.replace("hubtown-", "").replace("akruti-", "").replace("ackruti-", "")
    return f"Astra {parts.replace('-', ' ').title()}".strip()


def apply_content(text: str) -> str:
    for old, new in CONTENT_REPLACEMENTS:
        text = text.replace(old, new)
    return process_projects(text)


def apply_js(text: str) -> str:
    for old, new in JS_SAFE_REPLACEMENTS:
        text = text.replace(old, new)
    return text


def process_projects(text: str) -> str:
    for old_city, new_city in [
        ("mumbai", "karachi"),
        ("thane", "rawalpindi"),
        ("pune", "lahore"),
        ("gujarat", "lahore"),
        ("khalapur", "islamabad"),
        ("maharashtra", "karachi"),
    ]:
        text = re.sub(rf'(?<="city":)"{old_city}"', f'"{new_city}"', text)
        text = re.sub(rf'(?<="city":){old_city}(?=,|\}})', new_city, text)

    for slug_m in re.finditer(r'"slug"\s*:\s*"([a-z0-9-]+)"', text):
        slug = slug_m.group(1)
        if not any(x in slug for x in ("hubtown", "akruti", "ackruti", "25-", "breach", "bandra", "sunstream", "asmeeta", "dlf")):
            continue
        city = slug_to_city(slug)
        new_title = slug_to_title(slug)
        for prefix in ("Hubtown ", " Akruti ", "Akruti ", "Ackruti ", " Astra "):
            pass
        # Replace common title patterns
        base = slug.replace("hubtown-", "").replace("akruti-", "").replace("ackruti-", "")
        patterns = [
            f"Hubtown {base.replace('-', ' ').title()}",
            f" Akruti {base.replace('-', ' ').title()}",
            f"Akruti {base.replace('-', ' ').title()}",
            f"Ackruti {base.replace('-', ' ').title()}",
        ]
        for p in patterns:
            if p.strip() in text:
                text = text.replace(p, new_title)
    return text


def finalize(text: str) -> str:
    text = re.sub(r'"locationLatitude":\s*"[\d.]+"', '"locationLatitude":"24.8607"', text)
    text = re.sub(r'"locationLongitude":\s*"[\d.]+"', '"locationLongitude":"67.0011"', text)
    text = re.sub(r'"locationsLatitude":\s*"[\d.]+"', '"locationsLatitude":"24.8607"', text)
    text = re.sub(r'"locationsLongitude":\s*"[\d.]+"', '"locationsLongitude":"67.0011"', text)
    text = text.replace('lang="en"', 'lang="en-PK"')
    return text


def should_process(path: Path) -> bool:
    if any(p in path.parts for p in SKIP_DIRS):
        return False
    if path.suffix.lower() in NEVER_TOUCH_SUFFIXES and path.name != "site.webmanifest":
        return False
    if path.name == "localize_pk.py":
        return False
    return True


def main():
    changed = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or not should_process(path):
            continue
        suffix = path.suffix.lower()
        if suffix not in {".html", ".json", ".js", ".txt", ".webmanifest"} and path.name != "PREVIEW.txt":
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        if path.name == "PREVIEW.txt":
            updated = (
                "Astra Developments Pakistan — localized preview\n"
                "==================================================\n\n"
                f"Brand: {BRAND}\n"
                f"Tagline: {TAGLINE}\n"
                f"Domain: {DOMAIN} (deploy: {SITE_URL})\n\n"
                "Original template source: Hubtown India clone (content replaced; design unchanged)\n\n"
                "Preview server (caching proxy):\n"
                "  python serve_proxy.py\n"
                "  Then open: http://127.0.0.1:8765/\n"
            )
        elif "_nuxt" in path.parts and suffix == ".js":
            updated = apply_js(original)
        elif path.name == "site.webmanifest":
            updated = original.replace('"Hubtown"', f'"{BRAND_SHORT}"').replace('"name": "Hubtown"', f'"name": "{BRAND_SHORT}"')
        else:
            updated = apply_content(original)

        updated = finalize(updated)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)))

    print(f"Updated {len(changed)} files")


if __name__ == "__main__":
    main()
