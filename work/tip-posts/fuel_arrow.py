"""Fuel door arrow tip image. python3 -I fuel_arrow.py out.png"""
import math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H, S = 1080, 1350, 2
KO = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
NUM = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
F = lambda p, s: ImageFont.truetype(p, s * S)
AMBER = (255, 176, 46); WHITE = (238, 242, 250); DIM = (120, 128, 145); YEL = (255, 214, 92)

g = np.linspace(0, 1, H * S)[:, None]
arr = (np.array([24, 27, 34]) * (1 - g) + np.array([8, 9, 12]) * g)[:, None, :].repeat(W * S, 1)
im = Image.fromarray(arr.astype(np.uint8)).convert('RGBA')
# gauge glow
glow = Image.new('L', im.size, 0)
ImageDraw.Draw(glow).ellipse((190 * S, 230 * S, 890 * S, 930 * S), fill=90)
im.paste(Image.new('RGBA', im.size, (40, 60, 110, 255)), (0, 0), glow.filter(ImageFilter.GaussianBlur(90 * S)))
d = ImageDraw.Draw(im, 'RGBA')
P = lambda x, y: (x * S, y * S)

def tc(xy, s, font, fill):
    w = d.textlength(s, font=font); d.text((xy[0] * S - w / 2, xy[1] * S), s, font=font, fill=fill)

tc((W / 2, 70), '주유구 왼쪽? 오른쪽?', F(KO, 56), WHITE)
tc((W / 2, 150), '계기판에 이미 답이 있었음', F(KO, 40), YEL)

# gauge
cx, cy, R = 540, 640, 300
d.ellipse((*P(cx - R - 30, cy - R - 30), *P(cx + R + 30, cy + R + 30)), outline=(70, 76, 92), width=6 * S)
a0, a1 = 210, 330                      # degrees, PIL clockwise from 3 o'clock
d.arc((*P(cx - R, cy - R), *P(cx + R, cy + R)), a0, a0 + 18, fill=(230, 60, 60), width=14 * S)
d.arc((*P(cx - R, cy - R), *P(cx + R, cy + R)), a0 + 18, a1, fill=(200, 205, 215), width=10 * S)
for k in range(9):
    a = math.radians(a0 + (a1 - a0) * k / 8); L = 46 if k % 4 == 0 else 26
    x0, y0 = cx + (R - 8) * math.cos(a), cy + (R - 8) * math.sin(a)
    x1, y1 = cx + (R - 8 - L) * math.cos(a), cy + (R - 8 - L) * math.sin(a)
    d.line((*P(x0, y0), *P(x1, y1)), fill=WHITE, width=(7 if k % 4 == 0 else 4) * S)
for k, lab in [(0, 'E'), (8, 'F'), (4, '½')]:
    a = math.radians(a0 + (a1 - a0) * k / 8)
    tc((cx + (R - 100) * math.cos(a), cy + (R - 100) * math.sin(a) - 30), lab, F(NUM, 50), (230, 60, 60) if lab == 'E' else WHITE)
# needle near E
an = math.radians(a0 + (a1 - a0) * 0.12)
nx, ny = cx + (R - 40) * math.cos(an), cy + (R - 40) * math.sin(an)
d.line((*P(cx, cy), *P(nx, ny)), fill=(255, 80, 60), width=10 * S)
d.ellipse((*P(cx - 34, cy - 34), *P(cx + 34, cy + 34)), fill=(45, 50, 62), outline=(120, 128, 145), width=4 * S)

# fuel pump icon + arrow (center, below hub)
ix, iy = 560, 760
d.rounded_rectangle((*P(ix - 38, iy - 60), *P(ix + 30, iy + 62)), radius=8 * S, fill=AMBER)
d.rectangle((*P(ix - 26, iy - 46), *P(ix + 18, iy - 14)), fill=(24, 27, 34))
d.rectangle((*P(ix - 52, iy + 58), *P(ix + 44, iy + 70)), fill=AMBER)
d.line((*P(ix + 30, iy - 30), *P(ix + 58, iy - 6), *P(ix + 58, iy + 40), *P(ix + 72, iy + 40), *P(ix + 72, iy - 30)), fill=AMBER, width=8 * S, joint='curve')
# arrow ◀ left of icon
ax = ix - 110
d.polygon([P(ax - 26, iy), P(ax + 16, iy - 26), P(ax + 16, iy + 26)], fill=AMBER)
# highlight ring + callout
d.ellipse((*P(ax - 62, iy - 62), *P(ax + 52, iy + 62)), outline=YEL, width=7 * S)
d.line((*P(ax - 58, iy + 40), *P(250, 990)), fill=YEL, width=5 * S)
d.text(P(80, 995), '이 화살표 방향 = 주유구 위치', font=F(KO, 42), fill=YEL)

# car top view (front up), fuel door left-rear
bx, by = 540, 1185
d.rounded_rectangle((*P(bx - 70, by - 130), *P(bx + 70, by + 130)), radius=50 * S, fill=(70, 78, 96), outline=(150, 158, 178), width=4 * S)
d.rounded_rectangle((*P(bx - 52, by - 80), *P(bx + 52, by - 30)), radius=14 * S, fill=(30, 36, 48))
d.rounded_rectangle((*P(bx - 50, by + 50), *P(bx + 50, by + 92)), radius=12 * S, fill=(30, 36, 48))
for sx in (-1, 1):
    for sy in (-1, 1):
        d.rounded_rectangle((*P(bx + sx * 70 - 9, by + sy * 80 - 26), *P(bx + sx * 70 + 9, by + sy * 80 + 26)), radius=6 * S, fill=(20, 22, 28))
d.rectangle((*P(bx - 76, by + 20), *P(bx - 64, by + 48)), fill=AMBER)
d.polygon([P(bx - 150, by + 34), P(bx - 104, by + 6), P(bx - 104, by + 62)], fill=AMBER)
d.text(P(bx + 110, by + 10), '◀ 이면 왼쪽', font=F(KO, 36), fill=WHITE)
d.text(P(bx + 110, by + 60), '▶ 이면 오른쪽', font=F(KO, 36), fill=DIM)
tc((W - 150, 22), '@pathtorich7', F(KO, 26), (255, 255, 255, 110))
im.convert('RGB').resize((W, H), Image.LANCZOS).save(sys.argv[1])
