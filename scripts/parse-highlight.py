import re
import json

path = r"C:\Users\laerc\AppData\Local\Temp\ig-highlight.html"
with open(path, encoding="utf-8", errors="ignore") as f:
    html = f.read()

shortcodes = set(re.findall(r"instagram\.com/p/([A-Za-z0-9_-]+)", html))
print("shortcodes p/", shortcodes)

matches = re.findall(r'"shortcode":"([A-Za-z0-9_-]+)"', html)
print("shortcode json count", len(set(matches)))
print(list(set(matches))[:15])

if "Depoimentos" in html:
    print("found Depoimentos in html")
