"""Ctrl+Shift+T tip image. python3 -I reopen_tab.py out.png"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H, S = 1080, 1350, 2
KO = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
EN = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
F = lambda p, s: ImageFont.truetype(p, s * S)
P = lambda x, y: (x * S, y * S)
g = np.linspace(0, 1, H * S)[:, None]
arr = (np.array([244, 247, 252]) * (1 - g) + np.array([226, 233, 245]) * g)[:, None, :].repeat(W * S, 1)
im = Image.fromarray(arr.astype(np.uint8)).convert('RGBA')
d = ImageDraw.Draw(im, 'RGBA')
BLUE = (37, 99, 235); INK = (30, 36, 52); GRAY = (110, 120, 140)
def tc(x, y, s, font, fill):
    w = d.textlength(s, font=font); d.text((x * S - w / 2, y * S), s, font=font, fill=fill)

tc(W / 2, 70, '실수로 닫은 인터넷 창', F(KO, 56), INK)
tc(W / 2, 148, '3초 만에 살리는 법', F(KO, 62), BLUE)

# browser mockup
bx0, by0, bx1, by1 = 110, 270, 970, 600
sh = Image.new('L', im.size, 0); ImageDraw.Draw(sh).rounded_rectangle((*P(bx0 + 6, by0 + 14), *P(bx1 + 6, by1 + 14)), radius=24 * S, fill=70)
im.paste(Image.new('RGBA', im.size, (60, 70, 100, 255)), (0, 0), sh.filter(ImageFilter.GaussianBlur(18 * S)))
d = ImageDraw.Draw(im, 'RGBA')
d.rounded_rectangle((*P(bx0, by0), *P(bx1, by1)), radius=24 * S, fill=(255, 255, 255), outline=(205, 212, 226), width=2 * S)
d.rounded_rectangle((*P(bx0, by0), *P(bx1, by0 + 80)), radius=24 * S, fill=(232, 236, 244))
d.rectangle((*P(bx0, by0 + 50), *P(bx1, by0 + 80)), fill=(232, 236, 244))
for i, c in enumerate([(255, 95, 87), (255, 189, 46), (40, 200, 64)]):
    d.ellipse((*P(bx0 + 28 + i * 30, by0 + 28), *P(bx0 + 46 + i * 30, by0 + 46)), fill=c)
# tabs
d.rounded_rectangle((*P(bx0 + 140, by0 + 18), *P(bx0 + 390, by0 + 80)), radius=14 * S, fill=(255, 255, 255))
d.text(P(bx0 + 165, by0 + 32), '메일함', font=F(KO, 28), fill=INK)
# ghost tab (closed)
tx0 = bx0 + 400
for x in range(tx0, tx0 + 260, 22):
    d.line((*P(x, by0 + 20), *P(x + 11, by0 + 20)), fill=BLUE, width=3 * S)
d.line((*P(tx0, by0 + 20), *P(tx0, by0 + 78)), fill=BLUE, width=3 * S)
d.line((*P(tx0 + 260, by0 + 20), *P(tx0 + 260, by0 + 78)), fill=BLUE, width=3 * S)
d.text(P(tx0 + 22, by0 + 32), '방금 닫은 탭', font=F(KO, 28), fill=BLUE)
# content lines
d.rounded_rectangle((*P(bx0 + 40, by0 + 120), *P(bx1 - 40, by0 + 170)), radius=25 * S, fill=(240, 243, 249))
for k, wv in enumerate([620, 540, 680, 420]):
    d.rounded_rectangle((*P(bx0 + 40, by0 + 205 + k * 30), *P(bx0 + 40 + wv, by0 + 220 + k * 30)), radius=7 * S, fill=(228, 233, 242))
# revive arrow
ax, ay = tx0 + 310, by0 + 49
d.arc((*P(ax - 24, ay - 24), *P(ax + 24, ay + 24)), 60, 330, fill=BLUE, width=6 * S)
d.polygon([P(ax + 18, ay - 30), P(ax + 34, ay - 6), P(ax + 8, ay - 8)], fill=BLUE)

# keycaps
def key(x0, w, label, size):
    y0, h = 720, 170
    d.rounded_rectangle((*P(x0, y0 + 14), *P(x0 + w, y0 + h + 14)), radius=26 * S, fill=(170, 180, 200))
    d.rounded_rectangle((*P(x0, y0), *P(x0 + w, y0 + h)), radius=26 * S, fill=(255, 255, 255), outline=(200, 208, 222), width=2 * S)
    f = F(EN, size); tw = d.textlength(label, font=f) / S
    d.text(((x0 + w / 2 - tw / 2) * S, (y0 + h / 2 - size * 0.62) * S), label, font=f, fill=INK)
key(70, 270, 'Ctrl', 66); tc(375, 765, '+', F(EN, 70), GRAY)
key(420, 330, 'Shift', 66); tc(785, 765, '+', F(EN, 70), GRAY)
key(830, 180, 'T', 84)
d.rounded_rectangle((*P(830 - 8, 720 - 8), *P(1010 + 8, 890 + 8)), radius=32 * S, outline=BLUE, width=6 * S)

tc(W / 2, 980, '누를 때마다 닫은 순서 거꾸로 하나씩 부활', F(KO, 38), INK)
d.rounded_rectangle((*P(250, 1060), *P(830, 1130)), radius=35 * S, fill=(255, 255, 255), outline=(205, 212, 226), width=2 * S)
f1, f2 = F(KO, 38), F('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 36)
t1, t2 = '맥은 ', 'Cmd ⌘ + Shift + T'
w1, w2 = d.textlength(t1, font=f1), d.textlength(t2, font=f2)
x = W * S / 2 - (w1 + w2) / 2
d.text((x, 1072 * S), t1, font=f1, fill=GRAY); d.text((x + w1, 1076 * S), t2, font=f2, fill=GRAY)
tc(W / 2, 1185, '크롬 · 엣지 · 웨일 · 파이어폭스 다 됨', F(KO, 32), GRAY)
tc(W - 150, 1290, '@pathtorich7', F(KO, 26), (90, 100, 125, 130))
im.convert('RGB').resize((W, H), Image.LANCZOS).save(sys.argv[1])
