import re

html = open(r"C:\Users\laerc\AppData\Local\Temp\ig-profile.html", encoding="utf-8", errors="ignore").read()
codes = set(re.findall(r'"shortcode":"([A-Za-z0-9_-]{11})"', html))
print("count", len(codes))
print(list(codes)[:12])
