import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(
    r"c:\Users\laerc\Documents\0-Treinamentos e Pós\0- Pós Graduação\4 - Pós Graduação IA & Estratégia\1- Projetos (aulas)\11- Site MANOLO"
)
SHARE_URL = "https://share.google/lH3b8jPVgYifp3KuI"
MAPS_SEARCH = "https://www.google.com/maps/search/Split+Motorsport?hl=pt-BR"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9",
}


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def extract_reviews(html):
    reviews = []
    seen = set()

    # Common escaped review text patterns in Google Maps payloads
    patterns = [
        r'\[\s*"([^"]{25,500})"\s*,\s*null\s*,\s*null\s*,\s*null\s*,\s*(\d)\s*\]',
        r'"reviewBody"\s*:\s*"([^"]{20,500})"',
        r'"description"\s*:\s*"([^"]{20,500})"\s*,\s*"reviewRating"',
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, html):
            text = match.group(1).replace("\\n", " ").replace("\\u0026", "&").strip()
            stars = int(match.group(2)) if match.lastindex and match.lastindex >= 2 and match.group(2).isdigit() else 5
            if text in seen or len(text) < 20:
                continue
            if any(x in text.lower() for x in ["function(", "google", "http", "null"]):
                continue
            seen.add(text)
            reviews.append({"text": text, "rating": stars})

    # Author + text pairs
    author_pairs = re.findall(
        r'"([^"]{2,40})"\s*,\s*(\d)\s*,\s*null\s*,\s*"([^"]{20,400})"',
        html,
    )
    for author, stars, text in author_pairs:
        text = text.replace("\\n", " ").strip()
        if text in seen:
            continue
        seen.add(text)
        reviews.append(
            {
                "author": author,
                "rating": int(stars),
                "text": text,
            }
        )

    return reviews[:6]


html = fetch(MAPS_SEARCH)
reviews = extract_reviews(html)

rating_match = re.search(r"(\d,\d|\d\.\d)\s*\(\d+\)", html)
rating = rating_match.group(1).replace(",", ".") if rating_match else "5.0"
count_match = re.search(r"(\d+)\s*avalia", html, re.I)
review_count = int(count_match.group(1)) if count_match else len(reviews)

maps_match = re.search(r"https://www\\.google\\.com/maps/place/[^\"\\\\]+", html)
maps_url = maps_match.group(0).replace("\\u0026", "&") if maps_match else MAPS_SEARCH

payload = {
    "businessName": "Split Motorsport",
    "sourceUrl": SHARE_URL,
    "mapsUrl": maps_url,
    "kgmid": "/g/11w4qt5p52",
    "rating": float(rating),
    "reviewCount": review_count,
    "reviews": reviews,
}

out = ROOT / "data" / "google-reviews.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

print("reviews found:", len(reviews))
print("rating:", rating, "count:", review_count)
for r in reviews[:3]:
    print("-", r.get("author", "?"), r["text"][:80])
