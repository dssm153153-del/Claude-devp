"""Banana stem wrap tip image. python3 -I banana_wrap.py out.png"""
import math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H, S = 1080, 1350, 2
KO = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
F = lambda s: ImageFont.truetype(KO, s * S)
rng = np.random.default_rng(7)

g = np.linspace(0, 1, H * S)[:, None]
arr = (np.array([252, 246, 232]) * (1 - g) + np.array([240, 228, 205]) * g)[:, None, :].repeat(W * S, 1)
im = Image.fromarray(arr.astype(np.uint8)).convert('RGBA')
d = ImageDraw.Draw(im, 'RGBA')
P = lambda x, y: (x * S, y * S)
def tc(x, y, s, font, fill):
    w = d.textlength(s, font=font); d.text((x * S - w / 2, y * S), s, font=font, fill=fill)

# table
d.rectangle((*P(0, 1090), *P(W, H)), fill=(196, 150, 104))
for y in range(1100, H, 46):
    d.line((*P(0, y), *P(W, y + 6)), fill=(176, 132, 90), width=3 * S)
d.rectangle((*P(0, 1086), *P(W, 1096)), fill=(160, 116, 76))

tc(W / 2, 40, '바나나 꼭지에 랩 감으면', F(54), (60, 45, 30))
tc(W / 2, 110, '진짜 덜 익을까?', F(64), (214, 120, 20))

def banana(cx, cy, ang, length, width, ripe):
    """curved banana from crown (cx,cy) going in direction ang (deg)."""
    L = Image.new('L', im.size, 0); ld = ImageDraw.Draw(L)
    n = 48; x, y = cx, cy; ds = length / n
    pts_o, pts_i = [], []
    for k in range(n + 1):
        u = k / n
        phi = math.radians(ang - 55 * u)
        if k: x += ds * math.cos(phi); y += ds * math.sin(phi)
        wdt = width * max(0.42 if u < 0.5 else 0.12, math.sin(math.pi * u) ** 0.55)
        nx, ny = -math.sin(phi), math.cos(phi)
        pts_o.append(((x + nx * wdt / 2) * S, (y + ny * wdt / 2) * S))
        pts_i.append(((x - nx * wdt / 2) * S, (y - ny * wdt / 2) * S))
    ld.polygon(pts_o + pts_i[::-1], fill=255)
    tip = pts_o[-1]
    base = np.array([250, 214, 60]) if ripe < 0.5 else np.array([236, 186, 60])
    col = Image.new('RGBA', im.size, (*base, 255))
    cd = ImageDraw.Draw(col, 'RGBA')
    # ridge highlight
    cd.line([((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 - 4 * S) for p, q in zip(pts_o, pts_i)], fill=(255, 240, 150, 160), width=int(width * 0.18) * S)
    cd.line(pts_o, fill=(200, 150, 30, 200), width=4 * S)
    # spots
    nsp = int(ripe * 70)
    for _ in range(nsp):
        k = rng.integers(3, n - 2); p, q = pts_o[k], pts_i[k]; t = rng.random()
        x, y = p[0] * t + q[0] * (1 - t), p[1] * t + q[1] * (1 - t); r = rng.uniform(3, 9) * S * (0.6 + ripe)
        cd.ellipse((x - r, y - r * 0.7, x + r, y + r * 0.7), fill=(110, 70, 30, int(150 + 80 * ripe)))
    im.paste(col, (0, 0), L)
    d2 = ImageDraw.Draw(im, 'RGBA')
    d2.ellipse((tip[0] - 7 * S, tip[1] - 7 * S, tip[0] + 7 * S, tip[1] + 7 * S), fill=(70, 50, 30))

def bunch(cx, cy, ripe, wrapped):
    for ang, ln in [(48, 300), (32, 325), (16, 335), (0, 315)]:
        banana(cx, cy, ang, ln, 92, ripe)
    d2 = ImageDraw.Draw(im, 'RGBA')
    # crown / stems
    stem = (120, 150, 60) if not wrapped else (120, 150, 60)
    d2.rounded_rectangle((*P(cx - 46, cy - 40), *P(cx + 18, cy + 34)), radius=14 * S, fill=stem if ripe < 0.5 else (110, 95, 50))
    d2.rounded_rectangle((*P(cx - 70, cy - 24), *P(cx - 30, cy + 10)), radius=8 * S, fill=(90, 110, 50) if ripe < 0.5 else (80, 60, 35))
    if wrapped:
        d2.rounded_rectangle((*P(cx - 62, cy - 52), *P(cx + 30, cy + 46)), radius=22 * S, fill=(235, 245, 255, 120), outline=(255, 255, 255, 230), width=4 * S)
        for k in range(3):
            d2.line((*P(cx - 50 + k * 26, cy - 44), *P(cx - 58 + k * 26, cy + 38)), fill=(255, 255, 255, 170), width=3 * S)
        d2.line((*P(cx - 40, cy - 46), *P(cx + 6, cy - 46)), fill=(255, 255, 255, 255), width=5 * S)

# panels
for x0, title, ripe, wr, tag in [(40, '그냥 둔 바나나', 0.95, False, (150, 80, 40)), (560, '꼭지만 랩 감은 바나나', 0.08, True, (40, 140, 90))]:
    d.rounded_rectangle((*P(x0, 275), *P(x0 + 480, 1060)), radius=34 * S, fill=(255, 255, 255, 150), outline=(230, 214, 190), width=3 * S)
    tc(x0 + 240, 300, title, F(38), (70, 55, 40))
    bunch(x0 + 95, 680, ripe, wr)
    d = ImageDraw.Draw(im, 'RGBA')
    lab = '갈색 반점 가득' if not wr else '아직 노랗고 탱탱'
    tc(x0 + 240, 980, lab, F(34), tag)
d.rounded_rectangle((*P(420, 206), *P(660, 252)), radius=24 * S, fill=(70, 55, 40))
tc(540, 211, '며칠 뒤 (예시)', F(30), (255, 240, 210))

tc(W / 2, 1150, '숙성 가스(에틸렌)가 꼭지에서 많이 나와서래', F(36), (255, 250, 240))
tc(W / 2, 1215, '효과가 크다 vs 별 차이 없다, 의견 갈림', F(30), (255, 230, 190))
tc(W - 150, 1295, '@pathtorich7', F(26), (255, 245, 230, 150))
im.convert('RGB').resize((W, H), Image.LANCZOS).save(sys.argv[1])
