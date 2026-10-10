"""Week1 code-made cards. python3 -I make_cards.py"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H, S = 1080, 1350, 2
KO = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
EN = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
F = lambda p, s: ImageFont.truetype(p, int(s * S))
P = lambda x, y: (x * S, y * S)
INK = (30, 36, 52); BLUE = (37, 99, 235); GRAY = (110, 120, 140); YEL = (255, 214, 92)

def grad(c0, c1):
    g = np.linspace(0, 1, H * S)[:, None]
    return Image.fromarray((np.array(c0) * (1 - g) + np.array(c1) * g)[:, None, :].repeat(W * S, 1).astype(np.uint8)).convert('RGBA')
def tc(d, x, y, s, font, fill):
    w = d.textlength(s, font=font); d.text((x * S - w / 2, y * S), s, font=font, fill=fill)
def save(im, name):
    im.convert('RGB').resize((W, H), Image.LANCZOS).save(name)
def wm(d, light=False):
    tc(d, W - 150, 1295, '@pathtorich7', F(KO, 26), (255, 255, 255, 140) if light else (90, 100, 125, 140))

def chalkboard():
    rng = np.random.default_rng(3)
    base = np.zeros((H * S, W * S, 3), np.float32); base[:] = (38, 62, 50)
    base += rng.normal(0, 6, (H * S, W * S, 1))
    sm = Image.fromarray((rng.random((H // 40, W // 40)) * 255).astype(np.uint8)).resize((W * S, H * S), Image.BICUBIC).filter(ImageFilter.GaussianBlur(30))
    base += (np.asarray(sm, np.float32)[..., None] - 128) * 0.12
    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert('RGBA')
    d = ImageDraw.Draw(im, 'RGBA')
    for i, c in enumerate([(120, 82, 48), (140, 98, 58)]):
        d.rectangle((i * 6 * S, i * 6 * S, (W - 1 - i * 6) * S, (H - 1 - i * 6) * S), outline=c, width=(40 - i * 12) * S)
    return im, d

# Quiz-03: 1=5 sequence
im, d = chalkboard()
CH = (240, 240, 232)
tc(d, W / 2, 150, '규칙을 찾아보세요', F(KO, 60), CH)
for i, s in enumerate(['1 = 5', '2 = 25', '3 = 125', '4 = 625', '5 = ?']):
    tc(d, W / 2, 330 + i * 165, s, F(EN, 104), YEL if i == 4 else CH)
tc(d, W / 2, 1170, '정답이 두 개라고 싸움 남', F(KO, 40), (200, 215, 205))
wm(d, True); save(im, 'Quiz-03-one-equals-five.png')

# Quiz-04: Muller-Lyer
im = grad((250, 247, 240), (236, 230, 218)); d = ImageDraw.Draw(im, 'RGBA')
tc(d, W / 2, 110, '위 선 vs 아래 선', F(KO, 62), INK)
tc(d, W / 2, 200, '어느 쪽이 더 길까?', F(KO, 62), (214, 90, 40))
L, x0 = 560, (W - 560) / 2
def line(y, out):
    d.line((*P(x0, y), *P(x0 + L, y)), fill=INK, width=12 * S)
    a = 70
    for x, sgn in [(x0, -1), (x0 + L, 1)]:
        dx = a * (sgn if out else -sgn)
        d.line((*P(x, y), *P(x + dx * 0.75, y - a * 0.75)), fill=INK, width=12 * S)
        d.line((*P(x, y), *P(x + dx * 0.75, y + a * 0.75)), fill=INK, width=12 * S)
line(520, True); line(860, False)
tc(d, 120, 490, 'A', F(EN, 56), GRAY); tc(d, 120, 830, 'B', F(EN, 56), GRAY)
tc(d, W / 2, 1060, '자 대고 재보기 전에 먼저 골라보기 ㅋㅋ', F(KO, 38), GRAY)
wm(d); save(im, 'Quiz-04-line-illusion.png')

# Quiz-05: triangle count (answer 12)
im = grad((243, 246, 252), (224, 232, 246)); d = ImageDraw.Draw(im, 'RGBA')
tc(d, W / 2, 110, '삼각형은 모두 몇 개?', F(KO, 66), INK)
tc(d, W / 2, 205, '10초 안에 세보기', F(KO, 42), BLUE)
A = (540, 330); B1, B2 = (170, 1030), (910, 1030)
pts = [(B1[0] + (B2[0] - B1[0]) * k, 1030) for k in (0, 1 / 3, 2 / 3, 1)]
for p in pts: d.line((*P(*A), *P(*p)), fill=INK, width=9 * S)
d.line((*P(*B1), *P(*B2)), fill=INK, width=9 * S)
yh = 760; t = (yh - A[1]) / (1030 - A[1])
d.line((*P(A[0] + (B1[0] - A[0]) * t, yh), *P(A[0] + (B2[0] - A[0]) * t, yh)), fill=INK, width=9 * S)
tc(d, W / 2, 1110, '6개? 8개? 10개? 의견 갈림', F(KO, 40), GRAY)
wm(d); save(im, 'Quiz-05-triangles.png')

# shortcut cards
def keycard(name, title1, title2, keys, line1, line2, accent):
    im = grad((244, 247, 252), (226, 233, 245)); d = ImageDraw.Draw(im, 'RGBA')
    tc(d, W / 2, 120, title1, F(KO, 58), INK); tc(d, W / 2, 205, title2, F(KO, 64), accent)
    widths = [max(170, 60 + len(k) * 52) for k in keys]
    gap = 70; total = sum(widths) + gap * (len(keys) - 1); x = (W - total) / 2; y0 = 520
    for i, (k, w) in enumerate(zip(keys, widths)):
        d.rounded_rectangle((*P(x, y0 + 16), *P(x + w, y0 + 196)), radius=28 * S, fill=(165, 176, 198))
        d.rounded_rectangle((*P(x, y0), *P(x + w, y0 + 180)), radius=28 * S, fill=(255, 255, 255), outline=(200, 208, 222), width=2 * S)
        f = F(EN, 72 if len(k) > 1 else 92); tw = d.textlength(k, font=f) / S
        d.text(((x + w / 2 - tw / 2) * S, (y0 + 90 - (72 if len(k) > 1 else 92) * 0.62) * S), k, font=f, fill=INK)
        if i < len(keys) - 1: tc(d, x + w + gap / 2, y0 + 50, '+', F(EN, 70), GRAY)
        x += w + gap
    tc(d, W / 2, 860, line1, F(KO, 40), INK); tc(d, W / 2, 940, line2, F(KO, 34), GRAY)
    wm(d); save(im, name)
keycard('Tip-05-win-v.png', '복사한 거 덮어써서 날린 적 있음?', '복사 기록 다 꺼내보기', ['Win', 'V'],
        '최근에 복사한 것들이 목록으로 쫙 나옴', '처음 한 번 "켜기" 누르면 끝 · 윈도우 10/11', BLUE)
keycard('Tip-06-win-shift-s.png', '화면 캡처 아직도 프린트스크린?', '원하는 부분만 바로 캡처', ['Win', 'Shift', 'S'],
        '드래그한 영역만 캡처돼서 바로 붙여넣기 가능', '맥은 Cmd + Shift + 4', (214, 90, 40))
print('ok')
