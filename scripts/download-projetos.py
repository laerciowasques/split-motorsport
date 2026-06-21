import json
import re
import urllib.request
from pathlib import Path

API = "https://www.instagram.com/api/v1/users/web_profile_info/?username=split_motorsport"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "X-IG-App-ID": "936619743392459",
    "X-Requested-With": "XMLHttpRequest",
}

ROOT = Path(
    r"c:\Users\laerc\Documents\0-Treinamentos e Pós\0- Pós Graduação\4 - Pós Graduação IA & Estratégia\1- Projetos (aulas)\11- Site MANOLO"
)
OUT_DIR = ROOT / "images" / "projetos"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TAGS = [
    "Antes e depois",
    "Restauração mecânica",
    "Preparação leve",
    "Revisão diária",
    "Preservação original",
]

req = urllib.request.Request(API, headers=HEADERS)
with urllib.request.urlopen(req, timeout=30) as resp:
    data = json.loads(resp.read().decode("utf-8"))

edges = data["data"]["user"]["edge_owner_to_timeline_media"]["edges"][:5]
projects = []

for index, edge in enumerate(edges):
    node = edge["node"]
    shortcode = node["shortcode"]
    url = node["display_url"]
    caption = ""
    caption_edges = node.get("edge_media_to_caption", {}).get("edges", [])
    if caption_edges:
        caption = caption_edges[0]["node"]["text"].replace("\n", " ").strip()

    filename = f"projeto-{index + 1}.jpg"
    filepath = OUT_DIR / filename

    img_req = urllib.request.Request(url, headers={"User-Agent": HEADERS["User-Agent"]})
    with urllib.request.urlopen(img_req, timeout=60) as img_resp:
        filepath.write_bytes(img_resp.read())

    title = caption[:70] + ("…" if len(caption) > 70 else "") if caption else f"Projeto Split Motorsport {index + 1}"
    text = caption if caption else "Projeto realizado pela Split Motorsport."

    projects.append(
        {
            "file": f"images/projetos/{filename}",
            "tag": TAGS[index],
            "title": title,
            "text": text[:160] + ("…" if len(text) > 160 else ""),
            "alt": caption[:120] if caption else "Projeto Split Motorsport no Instagram",
            "instagram": f"https://www.instagram.com/p/{shortcode}/"
            if not node.get("is_video")
            else f"https://www.instagram.com/reel/{shortcode}/",
            "shortcode": shortcode,
        }
    )

(ROOT / "data" / "projetos.json").parent.mkdir(exist_ok=True)
(ROOT / "data" / "projetos.json").write_text(
    json.dumps(projects, ensure_ascii=False, indent=2), encoding="utf-8"
)

print("saved", len(projects), "images to", OUT_DIR)
