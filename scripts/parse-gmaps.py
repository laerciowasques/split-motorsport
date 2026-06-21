import re
from pathlib import Path

for name in ["gmaps-search.html", "google-share.html"]:
    path = Path(r"C:\Users\laerc\AppData\Local\Temp") / name
    if not path.exists():
        continue
    html = path.read_text(encoding="utf-8", errors="ignore")
    print("===", name, "===")
    print("ChIJ", re.findall(r"ChIJ[A-Za-z0-9_-]{20,}", html)[:5])
    print("place", re.findall(r"/maps/place/[^\"\\?]+", html)[:5])
    print("reviews", "review" in html.lower())
