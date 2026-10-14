"""초보운전 스티커 슬라이드 영상. python3 -I build_slides.py  (work/week2/video에서 실행)
1080x1350(4:5) 30fps. 장당 1.607초(112BPM 3박) 천천히 줌인, 컷마다 0.25초 밀기 전환 + 휙,
끝 카드 "몇 번이 제일 웃김?" 2초, 워터마크 @pathtorich7.
"""
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1350, 30
PER, TR, END = 1.607, 0.25, 2.0
KO = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
EN = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
AUD = '../../eunchae-video/audio/'
MUSIC, MUSIC_OFF, WHOOSH, WHOOSH_PEAK, SPARKLE = AUD + 'A1-Music-v2.mp3', 6.27, AUD + 'A2-Whoosh.mp3', 0.17, AUD + 'A3-Sparkle.mp3'
FILES = ['Sticker-V1.png', 'Sticker-V2.png', 'Sticker-V3.png', '../Sticker-AI-02-raw.png', 'Sticker-V4.png',
         'Sticker-V5.png', 'Sticker-V6.png', 'Sticker-V7.png', 'Sticker-V8.png', '../Sticker-AI-01-raw.png']
IW, IH = 1080, 810  # 4:3 슬롯
IY = (H - IH) // 2 + 40


def cover(im, w, h):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def text_c(d, y, s, font, fill, stroke=0):
    w = d.textlength(s, font=font)
    d.text(((W - w) / 2, y), s, font=font, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))


CROPS = {'../Sticker-AI-02-raw.png': (0, 0, 408, 250)}  # 아래 로고·번호판 제거
imgs = [Image.open(f).convert('RGB').crop(CROPS[f]) if f in CROPS else Image.open(f).convert('RGB') for f in FILES]
F_TITLE, F_NUM, F_END, F_WM = ImageFont.truetype(KO, 64), ImageFont.truetype(EN, 50), ImageFont.truetype(KO, 92), ImageFont.truetype(EN, 34)


def slide_bg(i):
    bg = cover(imgs[i], W, H).filter(ImageFilter.GaussianBlur(40))
    return Image.blend(bg, Image.new('RGB', (W, H), (0, 0, 0)), 0.45)


BGS = [slide_bg(i) for i in range(len(imgs))]


def slide(i, t):
    """i번 슬라이드, 등장 후 t초. 1.0→1.07 줌인."""
    f = BGS[i].copy()
    z = 1.0 + 0.07 * min(t / PER, 1.2)
    sw, sh = IW / z, IH / z
    im = cover(imgs[i], IW, IH)
    im = im.crop(((IW - sw) / 2, (IH - sh) / 2, (IW + sw) / 2, (IH + sh) / 2)).resize((IW, IH), Image.LANCZOS)
    f.paste(im, (0, IY))
    d = ImageDraw.Draw(f)
    text_c(d, 70, '초보운전 스티커 레전드 ㅋㅋ', F_TITLE, (255, 255, 255), 3)
    n = str(i + 1)
    r = 46
    cx, cy = W // 2, IY - 64
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 214, 0))
    w = d.textlength(n, font=F_NUM)
    d.text((cx - w / 2, cy - 31), n, font=F_NUM, fill=(20, 20, 20))
    return f


def end_card(t):
    f = BGS[-1].copy()
    f = Image.blend(f, Image.new('RGB', (W, H), (0, 0, 0)), 0.3)
    d = ImageDraw.Draw(f)
    s = min(1.0, 0.6 + t * 4)
    font = ImageFont.truetype(KO, int(130 * s))
    text_c(d, H / 2 - 160 * s, '몇 번이', font, (255, 255, 255), 5)
    text_c(d, H / 2 + 10 * s, '제일 웃김?', font, (255, 214, 0), 5)
    return f


def watermark(f):
    d = ImageDraw.Draw(f, 'RGBA')
    s = '@pathtorich7'
    w = d.textlength(s, font=F_WM)
    d.text((W - w - 34 + 2, H - 70 + 2), s, font=F_WM, fill=(0, 0, 0, 90))
    d.text((W - w - 34, H - 70), s, font=F_WM, fill=(255, 255, 255, 140))
    return f


N = len(imgs)
TOTAL = N * PER + END
cuts = [k * PER for k in range(1, N + 1)]  # 마지막 컷 = 끝 카드


def frame(t):
    k = min(int(t // PER), N)
    lt = t - k * PER
    cur = end_card(lt) if k == N else slide(k, lt)
    if k > 0 and lt < TR:  # 왼쪽으로 밀기 전환
        p = lt / TR
        p = 1 - (1 - p) ** 3
        prev = slide(k - 1, PER + lt)
        out = Image.new('RGB', (W, H))
        x = int(W * p)
        out.paste(prev, (-x, 0))
        out.paste(cur, (W - x, 0))
        cur = out
    return watermark(cur)


tmp = 'slides-noaudio.mp4'
p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                      '-i', '-', '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
for i in range(round(TOTAL * FPS)):
    p.stdin.write(np.asarray(frame(i / FPS)).tobytes())
p.stdin.close(); p.wait()

# 오디오: 음악 + 컷마다 휙(정점을 컷에 맞춤) + 끝 카드 반짝
inputs = ['-i', tmp, '-ss', str(MUSIC_OFF), '-t', str(TOTAL), '-i', MUSIC]
fil = [f'[1:a]volume=0.8,afade=t=out:st={TOTAL - 0.8}:d=0.8[m]']
mix = ['[m]']
for j, c in enumerate(cuts[:-1]):
    inputs += ['-i', WHOOSH]
    ms = int(max(0, c - WHOOSH_PEAK) * 1000)
    fil.append(f'[{j + 2}:a]atrim=0:0.45,volume=0.45,adelay={ms}|{ms}[w{j}]')
    mix.append(f'[w{j}]')
inputs += ['-i', SPARKLE]
ms = int(cuts[-1] * 1000)
fil.append(f'[{len(cuts) + 1}:a]atrim=0:1.2,volume=0.6,adelay={ms}|{ms}[s]')
mix.append('[s]')
fil.append(''.join(mix) + f'amix=inputs={len(mix)}:normalize=0,alimiter=limit=0.9[a]')
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', *inputs, '-filter_complex', ';'.join(fil), '-map', '0:v', '-map', '[a]',
                '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', 'Sticker-Slides-v2.mp4'], check=True)
print('Sticker-Slides-v2.mp4', round(TOTAL, 2), 's')
