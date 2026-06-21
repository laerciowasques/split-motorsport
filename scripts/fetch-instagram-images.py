import json
import re
import urllib.request
from pathlib import Path

HTML = Path(r"C:\Users\laerc\AppData\Local\Temp\ig-split-profile.html")
OUT_DIR = Path(
    r"c:\Users\laerc\Documents\0-Treinamentos e Pós\0- Pós Graduação\4 - Pós Graduação IA & Estratégia\1- Projetos (aulas)\11- Site MANOLO\images\projetos"
)

html = HTML.read_text(encoding="utf-8", errors="ignore")

# Thumbnails from profile grid
thumb_urls = re.findall(
    r'"display_url":"(https:\\/\\/[^"]+?cdninstagram\\.com[^"]+?)"', html
)
thumb_urls += re.findall(
    r'"(https://[^"]+?cdninstagram\.com[^"]+\.(?:jpg|webp)[^"]*)"', html
)

clean = []
seen = set()
for url in thumb_urls:
    url = url.replace("\\u0026", "&").replace("\\/", "/")
    if "150x150" in url or "s150x150" in url:
        continue
    key = url.split("?")[0]
    if key not in seen and "cdninstagram.com" in url:
        seen.add(key)
        clean.append(url)

print("found", len(clean))
for u in clean[:10]:
    print(u[:140])

# Also try shortcodes
codes = re.findall(r'"shortcode":"([A-Za-z0-9_-]{11})"', html)
print("shortcodes", len(set(codes)), list(set(codes))[:8])
