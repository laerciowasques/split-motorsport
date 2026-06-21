import re
from pathlib import Path

html = Path(r"C:\Users\laerc\AppData\Local\Temp\google-share.html").read_text(encoding="utf-8", errors="ignore")
patterns = [
    r"https://www\.google\.com/maps/place/[^\"\\s<>]+",
    r"https://maps\.google\.com/[^\"\\s<>]+",
    r"ChIJ[A-Za-z0-9_-]+",
    r"Split Motorsport",
]
for p in patterns:
    found = re.findall(p, html)
    if found:
        print(p, found[:5])

print("len", len(html))
