"""10L/7L/3L water-split quiz animation. python3 -I water_quiz.py out.mp4"""
import math, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, S = 1080, 1920, 30, 2          # S = supersample
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
NUM = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
f = lambda p, s: ImageFont.truetype(p, s * S)

CAP = [10, 7, 3]
PX = 56                                    # px per liter (1x)
JW = 230
XS = [210, 540, 870]
BASE = 1500
POURS = [(0, 1), (1, 2), (2, 0)]           # 10->7, 7->3, 3->10  (state 6,4,0 then quiz)
T_INTRO, T_POUR, T_GAP, T_END = 1.4, 1.6, 0.3, 3.6

def states():
    st = [10, 0, 0]; out = [list(st)]
    for a, b in POURS:
        m = min(st[a], CAP[b] - st[b]); st[a] -= m; st[b] += m; out.append(list(st))
    return out
ST = states()
ease = lambda t: 0.5 - 0.5 * math.cos(math.pi * max(0, min(1, t)))

# background (static)
bg = Image.new('RGB', (W * S, H * S))
g = np.linspace(0, 1, H * S)[:, None]
top, bot = np.array([18, 24, 48]), np.array([6, 9, 20])
arr = (top * (1 - g) + bot * g)[:, None, :].repeat(W * S, 1)
bg = Image.fromarray(arr.astype(np.uint8))
glow = Image.new('L', (W * S, H * S), 0)
ImageDraw.Draw(glow).ellipse((W * S * 0.1, H * S * 0.45, W * S * 0.9, H * S * 0.95), fill=70)
glow = glow.filter(ImageFilter.GaussianBlur(120 * S))
bg = Image.composite(Image.new('RGB', bg.size, (40, 90, 160)), bg, glow)

def jar_rect(i, lift=0):
    h = CAP[i] * PX
    x0 = XS[i] - JW / 2; y1 = BASE - lift; return x0, y1 - h, x0 + JW, y1

def lift_of(i, pouring, prog):
    if pouring is None or POURS[pouring][0] != i: return 0
    a, b = POURS[pouring]
    need = max(60, (CAP[b] - CAP[a]) * PX + 110)
    up = ease(prog / 0.25) if prog < 0.85 else 1 - ease((prog - 0.85) / 0.15)
    return need * up

def text_c(d, xy, s, font, fill, stroke=0, sc=(0, 0, 0)):
    w = d.textlength(s, font=font)
    d.text((xy[0] * S - w / 2, xy[1] * S), s, font=font, fill=fill, stroke_width=stroke * S, stroke_fill=sc)

def frame(t):
    im = bg.copy(); d = ImageDraw.Draw(im, 'RGBA')
    # timeline
    k = 0; prog = 0.0; tt = t - T_INTRO
    seg = T_POUR + T_GAP
    pouring = None
    if tt > 0:
        k = min(int(tt // seg), len(POURS)); r = tt - k * seg
        if k < len(POURS) and r < T_POUR:
            pouring = k; prog = ease(r / T_POUR)
        elif k < len(POURS):
            k += 1
    lv = list(ST[k])
    if pouring is not None:
        a, b = POURS[pouring]; s0, s1 = ST[pouring], ST[pouring + 1]
        pp = ease((prog - 0.25) / 0.6)
        lv = [s0[j] + (s1[j] - s0[j]) * pp for j in range(3)]
    done = min(k, len(POURS))
    quiz = tt > len(POURS) * seg
    # header
    text_c(d, (W / 2, 150), '10L를 정확히', f(FONT, 66), (235, 240, 255))
    text_c(d, (W / 2, 235), '반반 나눌 수 있을까?', f(FONT, 66), (255, 214, 92))
    text_c(d, (W / 2, 345), '쓸 수 있는 건 10L · 7L · 3L 통 세 개뿐', f(FONT, 34), (150, 165, 200))
    # step chip
    chip = f'붓기 {done}회' if pouring is None else f'붓기 {pouring + 1}회'
    cw = d.textlength(chip, font=f(FONT, 34)) / S + 60
    d.rounded_rectangle(((W / 2 - cw / 2) * S, 420 * S, (W / 2 + cw / 2) * S, 482 * S), radius=31 * S, fill=(255, 255, 255, 22), outline=(255, 255, 255, 60), width=2 * S)
    text_c(d, (W / 2, 431), chip, f(FONT, 34), (220, 228, 255))
    # jars
    for i in range(3):
        lift = lift_of(i, pouring, prog)
        x0, y0, x1, y1 = jar_rect(i, lift)
        # liquid
        lh = lv[i] * PX
        if lh > 0.5:
            liq = Image.new('RGBA', im.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(liq)
            wave = [(x * S, (y1 - lh + 6 * math.sin(x / 38 + t * 5 + i)) * S) for x in np.linspace(x0 + 8, x1 - 8, 40)]
            ld.polygon(wave + [((x1 - 8) * S, (y1 - 8) * S), ((x0 + 8) * S, (y1 - 8) * S)], fill=(56, 189, 248, 230))
            ld.line(wave, fill=(186, 240, 255, 255), width=4 * S)
            im.alpha_composite(liq) if im.mode == 'RGBA' else im.paste(liq, (0, 0), liq)
            d = ImageDraw.Draw(im, 'RGBA')
        # glass
        d.rounded_rectangle((x0 * S, y0 * S, x1 * S, y1 * S), radius=26 * S, outline=(230, 240, 255, 200), width=5 * S)
        d.rectangle(((x0 + 22) * S, (y0 + 30) * S, (x0 + 34) * S, (y1 - 40) * S), fill=(255, 255, 255, 28))
        for L in range(1, CAP[i]):
            yy = y1 - L * PX
            d.line(((x1 - 34) * S, yy * S, (x1 - 12) * S, yy * S), fill=(255, 255, 255, 90), width=2 * S)
        # goal line at 5L
        if CAP[i] >= 5:
            yy = y1 - 5 * PX
            for xx in np.arange(x0 - 14, x1 + 14, 22):
                d.line((xx * S, yy * S, (xx + 11) * S, yy * S), fill=(255, 214, 92, 200), width=3 * S)
        text_c(d, (XS[i], y0 - 70), f'{CAP[i]}L', f(NUM, 46), (235, 240, 255))
        val = lv[i]
        sval = f'{val:.0f}' if pouring is None else f'{val:.1f}'
        text_c(d, (XS[i], BASE + 40), sval, f(NUM, 78), (255, 255, 255))
        text_c(d, (XS[i], BASE + 138), f'/ {CAP[i]}', f(NUM, 32), (130, 145, 180))
    text_c(d, (W / 2, BASE - 5 * PX - 52), '목표선 5L', f(FONT, 26), (255, 214, 92))
    # pour stream
    if pouring is not None and 0.27 < prog < 0.85:
        a, b = POURS[pouring]
        ax0, ay0, ax1, _ = jar_rect(a, lift_of(a, pouring, prog)); bx0, by0, bx1, _ = jar_rect(b)
        sx = ax1 - 10 if b > a else ax0 + 10; sy = ay0 + 6
        ex = (bx0 + bx1) / 2; ey = by0 + 20
        cx, cy = (sx + ex) / 2, min(sy, ey) - 90
        pts = [((1 - u) ** 2 * sx + 2 * (1 - u) * u * cx + u * u * ex, (1 - u) ** 2 * sy + 2 * (1 - u) * u * cy + u * u * ey) for u in np.linspace(0, 1, 50)]
        d.line([(x * S, y * S) for x, y in pts], fill=(56, 189, 248, 220), width=14 * S, joint='curve')
        d.line([(x * S, y * S) for x, y in pts], fill=(200, 245, 255, 200), width=4 * S, joint='curve')
    # quiz overlay
    if quiz:
        q = min(1, (tt - len(POURS) * seg) / 0.5)
        ov = Image.new('RGBA', im.size, (5, 8, 18, int(70 * q))); im.paste(ov, (0, 0), ov); d = ImageDraw.Draw(im, 'RGBA')
        pulse = 1 + 0.06 * math.sin(t * 6)
        text_c(d, (W / 2, 520 - 40 * (pulse - 1) * 10), '?', f(NUM, int(150 * pulse)), (255, 214, 92, int(255 * q)))
        text_c(d, (W / 2, 705), '여기서 다음 한 수는?', f(FONT, 58), (255, 255, 255, int(255 * q)))
        text_c(d, (W / 2, 785), '5L + 5L 만들려면 최소 몇 번 부어야 할까', f(FONT, 34), (190, 205, 235, int(255 * q)))
    text_c(d, (W - 150, 60), '@pathtorich7', f(FONT, 26), (255, 255, 255, 110))
    return im.resize((W, H), Image.LANCZOS)

def main(out):
    total = T_INTRO + len(POURS) * (T_POUR + T_GAP) + T_END
    n = int(total * FPS)
    p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(i / FPS).convert('RGB').tobytes())
    p.stdin.close(); p.wait(); print(out, round(total, 2), 's')

if __name__ == '__main__':
    main(sys.argv[1])
