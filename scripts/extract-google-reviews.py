import json
import re
from pathlib import Path

html = Path(r"C:\Users\laerc\AppData\Local\Temp\gmaps-split.html").read_text(encoding="utf-8", errors="ignore")

# Decode unicode escapes in chunks
decoded = html.encode("utf-8").decode("unicode_escape", errors="ignore")

reviews = []
seen = set()

# Pattern: author, rating number, ..., review text in Google Maps arrays
for match in re.finditer(
    r'\[null,"([^"]{2,40})",null,null,(\d),null,"([^"]{20,500})"',
    decoded,
):
    author, rating, text = match.groups()
    text = text.replace("\\n", " ").strip()
    if text in seen:
        continue
    seen.add(text)
    reviews.append(
        {
            "author": author,
            "rating": int(rating),
            "text": text,
        }
    )

# Rating summary
rating_match = re.search(r"(\d,\d)\((\d+)\)", decoded)
rating = float(rating_match.group(1).replace(",", ".")) if rating_match else 5.0
count = int(rating_match.group(2)) if rating_match else len(reviews)

payload = {
    "businessName": "Split Motorsport",
    "sourceUrl": "https://share.google/lH3b8jPVgYifp3KuI",
    "mapsUrl": "https://www.google.com/maps/search/Split+Motorsport?hl=pt-BR",
    "mapsEmbedUrl": "https://www.google.com/maps?q=Split+Motorsport&output=embed&hl=pt-BR",
    "rating": rating,
    "reviewCount": count,
    "reviews": reviews[:6],
}

out = Path(
    r"c:\Users\laerc\Documents\0-Treinamentos e Pós\0- Pós Graduação\4 - Pós Graduação IA & Estratégia\1- Projetos (aulas)\11- Site MANOLO\data\google-reviews.json"
)
out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

print("reviews", len(reviews))
print("rating", rating, "count", count)
for r in reviews[:5]:
    print("-", r["author"], r["text"][:90])
