import re
import urllib.request

urls = [
    "https://share.google/lH3b8jPVgYifp3KuI",
    "https://www.google.com/url?q=https://share.google/lH3b8jPVgYifp3KuI",
    "https://maps.app.goo.gl/lH3b8jPVgYifp3KuI",
]

for url in urls:
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            final = resp.geturl()
            html = resp.read().decode("utf-8", errors="ignore")
        print("URL:", url)
        print("FINAL:", final)
        print("ChIJ", re.findall(r"ChIJ[A-Za-z0-9_-]+", html)[:3])
        print("place", re.findall(r"/maps/place/[^\"\\?]+", html)[:2])
        print("---")
    except Exception as exc:
        print("URL:", url, "ERR:", exc)
