"""Ctrl+Shift+T animation. python3 -I reopen_tab_anim.py out.mp4"""
import math, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H, FPS, S = 1080, 1920, 30, 2
KO = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
EN = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
ENR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
F = lambda p, s: ImageFont.truetype(p, int(s * S))
P = lambda x, y: (x * S, y * S)
BLUE = (37, 99, 235); INK = (30, 36, 52); GRAY = (110, 120, 140); YEL = (255, 196, 0); RED = (235, 64, 52)
ease = lambda t: 0.5 - 0.5 * math.cos(math.pi * max(0, min(1, t)))
def back(t):
    t = max(0, min(1, t)); c = 1.7; return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2

g = np.linspace(0, 1, H * S)[:, None]
BG = Image.fromarray((np.array([240, 244, 251]) * (1 - g) + np.array([220, 228, 243]) * g)[:, None, :].repeat(W * S, 1).astype(np.uint8)).convert('RGBA')

TABS = ['메일', '회의자료', '보고서 마감', '장바구니']
X0, Y0, X1, Y1 = 70, 430, 1010, 1130          # browser window
TW = 210

def tc(d, x, y, s, font, fill):
    w = d.textlength(s, font=font); d.text((x * S - w / 2, y * S), s, font=font, fill=fill)

def frame(t):
    im = BG.copy(); d = ImageDraw.Draw(im, 'RGBA')
    # title
    tc(d, W / 2, 150, '실수로 탭 닫았을 때', F(KO, 60), INK)
    ttl2 = '이거 하나면 끝' if t < 4.6 else '닫은 탭 부활 단축키'
    tc(d, W / 2, 240, ttl2, F(KO, 64), BLUE)
    # window + shadow
    sh = Image.new('L', im.size, 0); ImageDraw.Draw(sh).rounded_rectangle((*P(X0 + 8, Y0 + 20), *P(X1 + 8, Y1 + 20)), radius=28 * S, fill=80)
    im.paste(Image.new('RGBA', im.size, (50, 60, 90, 255)), (0, 0), sh.filter(ImageFilter.GaussianBlur(22 * S)))
    d = ImageDraw.Draw(im, 'RGBA')
    d.rounded_rectangle((*P(X0, Y0), *P(X1, Y1)), radius=28 * S, fill=(255, 255, 255), outline=(205, 212, 226), width=2 * S)
    d.rounded_rectangle((*P(X0, Y0), *P(X1, Y0 + 96)), radius=28 * S, fill=(229, 234, 243))
    d.rectangle((*P(X0, Y0 + 60), *P(X1, Y0 + 96)), fill=(229, 234, 243))
    for i, c in enumerate([(255, 95, 87), (255, 189, 46), (40, 200, 64)]):
        d.ellipse((*P(X0 + 30 + i * 32, Y0 + 30), *P(X0 + 50 + i * 32, Y0 + 50)), fill=c)
    # tab 2 (보고서) presence
    if t < 1.75: pres = 1.0
    elif t < 2.05: pres = 1 - ease((t - 1.75) / 0.3)
    elif t < 3.55: pres = 0.0
    else: pres = back((t - 3.55) / 0.45)
    xs = X0 + 140
    for i, name in enumerate(TABS):
        w = TW * (pres if i == 2 else 1)
        if w < 4: continue
        active = (i == 2 and pres > 0.5) or (i == 1 and pres <= 0.5)
        ty0 = Y0 + 22
        fill = (255, 255, 255) if active else (229, 234, 243)
        d.rounded_rectangle((*P(xs, ty0), *P(xs + w - 8, Y0 + 96)), radius=14 * S, fill=fill)
        if not active:
            d.line((*P(xs + w - 8, ty0 + 18), *P(xs + w - 8, ty0 + 56)), fill=(200, 206, 220), width=2 * S)
        if w > 120:
            col = INK if i != 2 else (BLUE if t > 3.55 else INK)
            d.text(P(xs + 22, ty0 + 20), name, font=F(KO, 28), fill=col)
            d.text(P(xs + w - 46, ty0 + 16), '×', font=F(ENR, 30), fill=GRAY)
        if i == 2 and 3.55 < t < 4.6 and pres > 0.8:
            a = int(160 * (1 - abs((t - 3.9) / 0.7)))
            d.rounded_rectangle((*P(xs - 6, ty0 - 6), *P(xs + w - 2, Y0 + 100)), radius=18 * S, outline=(*YEL, max(0, a)), width=6 * S)
        xs += w
    # page content
    showing_report = pres > 0.5
    cy = Y0 + 140
    d.rounded_rectangle((*P(X0 + 40, cy), *P(X1 - 40, cy + 52)), radius=26 * S, fill=(240, 243, 249))
    if showing_report:
        d.text(P(X0 + 60, cy + 90), '2분기 보고서 (작성 중...)', font=F(KO, 40), fill=INK)
        for k, wv in enumerate([760, 700, 820, 520, 740, 640, 300]):
            d.rounded_rectangle((*P(X0 + 60, cy + 175 + k * 52), *P(X0 + 60 + wv, cy + 197 + k * 52)), radius=10 * S, fill=(222, 229, 241))
    else:
        d.text(P(X0 + 60, cy + 90), '회의자료', font=F(KO, 40), fill=GRAY)
        for k, wv in enumerate([500, 620, 420]):
            d.rounded_rectangle((*P(X0 + 60, cy + 175 + k * 52), *P(X0 + 60 + wv, cy + 197 + k * 52)), radius=10 * S, fill=(236, 240, 247))
    # "앗" pop
    if 1.95 < t < 3.5:
        k = back((t - 1.95) / 0.3)
        f = F(KO, 92 * k)
        tc(d, W / 2, 720, '앗...!', f, (*RED, 255))
        tc(d, W / 2, 840, '1시간 쓴 보고서 날아감', F(KO, 40), (*RED, 220))
    if 3.55 < t < 4.6:
        k = back((t - 3.55) / 0.35)
        tc(d, W / 2, 760, '살아났다!' if k > 0 else '', F(KO, 80 * k), (*BLUE, 255))
    # cursor
    if t < 2.1:
        u = ease((t - 0.4) / 1.0)
        cx = 760 + (X0 + 140 + 2 * TW + TW - 30 - 760) * u
        cy2 = 1050 + (Y0 + 52 - 1050) * u
        if 1.5 < t < 1.7: cy2 += 4
        pts = [(cx, cy2), (cx, cy2 + 52), (cx + 14, cy2 + 40), (cx + 26, cy2 + 64), (cx + 36, cy2 + 59), (cx + 24, cy2 + 36), (cx + 42, cy2 + 36)]
        d.polygon([P(x, y) for x, y in pts], fill=(20, 20, 20), outline=(255, 255, 255))
        if 1.5 < t < 1.8:
            r = 20 + 60 * (t - 1.5)
            d.ellipse((*P(cx - r, cy2 - r), *P(cx + r, cy2 + r)), outline=(*BLUE, int(200 * (1 - (t - 1.5) / 0.3))), width=4 * S)
    # keycaps
    if t > 2.2:
        ap = ease((t - 2.2) / 0.3)
        ky = 1300 + 60 * (1 - ap)
        keys = [('Ctrl', 90, 270, 2.6), ('Shift', 420, 300, 2.95), ('T', 800, 190, 3.3)]
        for i, (lab, x, w, tp) in enumerate(keys):
            pressed = tp < t < 3.75 if t < 4.6 else True
            dy = 12 if (pressed and t < 4.6) else 0
            glow = pressed
            if i < 2:
                tc(d, x + w + (420 - 90 - 270) / 2 if i == 0 else x + w + (800 - 420 - 300) / 2, ky + 40, '+', F(EN, 64), (*GRAY, int(255 * ap)))
            d.rounded_rectangle((*P(x, ky + 16), *P(x + w, ky + 176)), radius=26 * S, fill=(160, 172, 196, int(255 * ap)))
            top = (255, 244, 200) if glow else (255, 255, 255)
            d.rounded_rectangle((*P(x, ky + dy), *P(x + w, ky + 160 + dy)), radius=26 * S, fill=(*top, int(255 * ap)), outline=(*(YEL if glow else (200, 208, 222)), int(255 * ap)), width=(6 if glow else 2) * S)
            f = F(EN, 66 if len(lab) > 1 else 84); tw = d.textlength(lab, font=f) / S
            d.text(((x + w / 2 - tw / 2) * S, (ky + 80 + dy - (0.62 * (66 if len(lab) > 1 else 84))) * S), lab, font=f, fill=(*INK, int(255 * ap)))
    if t > 4.6:
        a = int(255 * ease((t - 4.6) / 0.4))
        tc(d, W / 2, 1540, '누를 때마다 닫은 순서 거꾸로 하나씩 부활', F(KO, 38), (*INK, a))
        tc(d, W / 2, 1610, '맥은 Cmd + Shift + T · 크롬 엣지 웨일 다 됨', F(KO, 34), (*GRAY, a))
    tc(d, W - 150, 1840, '@pathtorich7', F(KO, 28), (90, 100, 125, 140))
    return im.resize((W, H), Image.LANCZOS)

def main(out, total=7.0):
    p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(int(total * FPS)):
        p.stdin.write(frame(i / FPS).convert('RGB').tobytes())
    p.stdin.close(); p.wait(); print(out)

if __name__ == '__main__':
    main(sys.argv[1])
