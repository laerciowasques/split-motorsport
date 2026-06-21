import re
from pathlib import Path

html = Path(r"C:\Users\laerc\AppData\Local\Temp\gmaps-split.html").read_text(encoding="utf-8", errors="ignore")

# Find Portuguese review-like strings near rating numbers
chunks = re.findall(r'"((?:[^"\\]|\\.){30,350})"', html)
reviews = []
seen = set()
for chunk in chunks:
    text = bytes(chunk, "utf-8").decode("unicode_escape", errors="ignore")
    text = text.replace("\\n", " ").strip()
    if len(text) < 35 or len(text) > 320:
        continue
    lower = text.lower()
    if not any(k in lower for k in ["fusca", "oficina", "motor", "servi", "excel", "recom", "profis", "atend", "split", "vw", "ar"]):
        continue
    if any(k in lower for k in ["function", "google", "http", "javascript", "svg"]):
        continue
    if text in seen:
        continue
    seen.add(text)
    reviews.append(text)

print("candidates", len(reviews))
for r in reviews[:10]:
    print("-", r[:120])
