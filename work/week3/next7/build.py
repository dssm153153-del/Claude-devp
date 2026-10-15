"""마스카라 커플: K1(0–9.7, 앞부분 1.25배속) + K2 + 자막 + 워터마크 (+음악) -> final/Next7-Draft-v1.mp4"""
import subprocess, os, sys
F = '/usr/share/fonts/truetype/nanum/NanumSquareEB.ttf'
MUSIC = sys.argv[1] if len(sys.argv) > 1 else None   # 음악 파일(없으면 무음)
OUT = sys.argv[2] if len(sys.argv) > 2 else 'final/Next7-Draft-v1.mp4'
HOLD = 0.6
SEG = [('clips/Next7-K1.mp4', 0.0, 6.5, 1.25), ('clips/Next7-K1.mp4', 6.5, 9.7, 1.0), ('clips/Next7-K2.mp4', 0.0, 5.167, 1.0)]
LEN = sum((b - a) / s for _, a, b, s in SEG) + HOLD
SUBS = [  # (시작, 끝, 화자, 문구)  K2 시작 = 8.4초
    (1.0, 5.2, 'him', '남편: 아~ 이렇게 하는 거지?'),
    (5.3, 6.8, 'her', '아내: …지금 놀려?'),
    (6.8, 8.4, 'her', '아내: 너 면도할 때 이러잖아'),
    (9.2, 11.4, 'her', '아내: 나가'),
    (11.8, LEN, 'her', '아내: 입은 원래 벌어지는 거야'),
]
os.makedirs('build', exist_ok=True)
cmd = ['ffmpeg', '-v', 'error', '-y']
for f in sorted({s[0] for s in SEG}): cmd += ['-i', f]
idx = {f: i for i, f in enumerate(sorted({s[0] for s in SEG}))}
fc = [f'[{idx[f]}:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{s},scale=1080:1890,pad=1080:1920:0:15:color=white,fps=30[s{i}]'
      for i, (f, a, b, s) in enumerate(SEG)]
v = ''.join(f'[s{i}]' for i in range(len(SEG))) + f'concat=n={len(SEG)}:v=1:a=0,tpad=stop_mode=clone:stop_duration={HOLD}'
for i, (a, b, who, t) in enumerate(SUBS):
    p = f'build/sub{i}.txt'; open(p, 'w').write(t)
    y, col = ('150', '#FFE14D') if who == 'him' else ('h*0.80', 'white')
    v += (f",drawtext=fontfile={F}:textfile={p}:fontsize=70:fontcolor={col}:borderw=7:bordercolor=black:"
          f"x=(w-tw)/2:y={y}:enable='between(t,{a},{b})'")
v += f",drawtext=fontfile={F}:text='@pathtorich7':fontsize=38:fontcolor=white@0.6:borderw=1:bordercolor=black@0.3:x=w-tw-36:y=40[v]"
fc.append(v)
if MUSIC:
    cmd += ['-i', MUSIC]
    fc.append(f'[{len(idx)}:a]atrim=0:{LEN},asetpts=PTS-STARTPTS,afade=t=out:st={LEN-0.6}:d=0.6[a]')
else:
    fc.append(f'anoisesrc=color=pink:amplitude=0.0:duration={LEN}[a]')
cmd += ['-filter_complex', ';'.join(fc), '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '23', '-preset', 'slow',
        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', '-t', f'{LEN:.3f}', OUT]
subprocess.run(cmd, check=True)
print(OUT, round(LEN, 2))
