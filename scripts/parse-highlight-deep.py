import re
import json

html = open(r"C:\Users\laerc\AppData\Local\Temp\ig-highlight.html", encoding="utf-8", errors="ignore").read()

patterns = [
    r'"id":"(\d{10,})"',
    r'"pk":"(\d{10,})"',
    r'"media_id":"(\d+)"',
    r'"code":"([A-Za-z0-9_-]{11})"',
    r'"shortcode":"([A-Za-z0-9_-]{11})"',
    r"instagram\.com/reel/([A-Za-z0-9_-]+)",
    r"instagram\.com/p/([A-Za-z0-9_-]+)",
]

for p in patterns:
    found = set(re.findall(p, html))
    if found:
        print(p, len(found), list(found)[:5])

if "17962501514442570" in html:
    print("highlight id found in html")
