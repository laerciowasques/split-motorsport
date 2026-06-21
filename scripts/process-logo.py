"""Remove fundo branco do logo e recorta margens transparentes."""
from collections import deque
from PIL import Image

INPUT = r"c:\Users\laerc\Documents\0-Treinamentos e Pós\0- Pós Graduação\4 - Pós Graduação IA & Estratégia\1- Projetos (aulas)\11- Site MANOLO\images\logo-split.png"
OUTPUT = INPUT

img = Image.open(INPUT).convert("RGBA")
pixels = img.load()
w, h = img.size


def is_background(r, g, b, a):
    return a > 0 and r >= 225 and g >= 225 and b >= 225


visited = set()
queue = deque()

for seed in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
    r, g, b, a = pixels[seed]
    if is_background(r, g, b, a) and seed not in visited:
        visited.add(seed)
        queue.append(seed)

while queue:
    x, y = queue.popleft()
    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        if nx < 0 or ny < 0 or nx >= w or ny >= h or (nx, ny) in visited:
            continue
        r, g, b, a = pixels[nx, ny]
        if is_background(r, g, b, a):
            visited.add((nx, ny))
            queue.append((nx, ny))

for x, y in visited:
    pixels[x, y] = (8, 8, 8, 0)

bbox = img.getbbox()
if bbox:
    img = img.crop(bbox)

img.save(OUTPUT, "PNG", optimize=True)
print("Processed:", OUTPUT, "new size:", img.size)
