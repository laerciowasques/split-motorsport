import re
from pathlib import Path

for name in ["gmaps-split.html", "gmaps-search.html"]:
    path = Path(r"C:\Users\laerc\AppData\Local\Temp") / name
    if not path.exists():
        continue
    html = path.read_text(encoding="utf-8", errors="ignore")
    print("===", name, "size", len(html))
    for pat in [
        r"ChIJ[A-Za-z0-9_-]+",
        r"0x[a-f0-9]+:0x[a-f0-9]+",
        r"Split Motorsport",
        r"11w4qt5p52",
        r"!1s[^!]+",
    ]:
        found = re.findall(pat, html)[:3]
        if found:
            print(pat, found)
