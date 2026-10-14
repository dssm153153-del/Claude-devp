"""제이크 아기 안 줌: K1 + 자막 + 효과음 + 워터마크 -> final/Baby-Final-v2.mp4"""
import subprocess, os
F = '/usr/share/fonts/truetype/nanum/NanumSquareEB.ttf'
HOLD = 0.8; LEN = 10.125 + HOLD
SUBS = [  # (시작, 끝, 화자, 문구)
    (0.0, 2.2, 'mom', '엄마: 제이크, 내 아기 돌려줘'),
    (2.2, 3.4, 'mom', '엄마: 제이크, 내 아기 돌려줘'),
    (2.2, 3.4, 'jake', '제이크: 싫어'),
    (3.4, 6.8, 'mom', '엄마: 걔 내 아기라니까?'),
    (4.5, 6.8, 'jake', '제이크: 싫다고오오~'),
    (7.0, LEN, 'mom', '엄마: 내 아기라고!!'),
    (8.3, LEN, 'jake', '제이크: (못 들은 척 꼭 안음)'),
]
os.makedirs('build', exist_ok=True)
vf = ['[0:v]scale=1097:1920,crop=1080:1920,fps=30,tpad=stop_mode=clone:stop_duration=%s' % HOLD]
for i, (a, b, who, t) in enumerate(SUBS):
    p = f'build/sub{i}.txt'; open(p, 'w').write(t)
    y, col = ('h*0.80', 'white') if who == 'mom' else ('150', '#FFE14D')
    vf.append(f"drawtext=fontfile={F}:textfile={p}:fontsize=70:fontcolor={col}:borderw=7:bordercolor=black:"
              f"x=(w-tw)/2:y={y}:enable='between(t,{a},{b})'")
vf.append(f"drawtext=fontfile={F}:text='@pathtorich7':fontsize=38:fontcolor=white@0.5:x=w-tw-36:y=40[v]")
SFX = [  # (파일, trim 시작, 끝, 위치, 볼륨)
    ('audio/S4-Giggle.mp3', 0.0, 2.75, 0.1, 0.5),
    ('audio/S3-Talkback.mp3', 2.38, 2.68, 2.2, 0.6),
    ('audio/S4-Giggle.mp3', 0.25, 1.8, 2.9, 0.4),
    ('audio/S3-Talkback.mp3', 0.15, 2.68, 4.4, 0.9),
    ('audio/S4-Giggle.mp3', 0.25, 2.75, 7.0, 0.6),
    ('audio/S4-Giggle.mp3', 2.0, 2.75, 9.9, 0.45),
]
cmd = ['ffmpeg', '-v', 'error', '-y', '-i', 'clips/Baby-K1.mp4']
af = [f'anoisesrc=color=pink:amplitude=0.006:duration={LEN}[n]']
for i, (f, a, b, at, vol) in enumerate(SFX):
    cmd += ['-i', f]
    af.append(f'[{i+1}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=out:st={b-a-0.25}:d=0.25,'
              f'volume={vol},adelay={int(at*1000)}:all=1[s{i}]')
af.append('[n]' + ''.join(f'[s{i}]' for i in range(len(SFX))) + f'amix=inputs={len(SFX)+1}:normalize=0,atrim=0:{LEN}[a]')
cmd += ['-filter_complex', ','.join(vf) + ';' + ';'.join(af), '-map', '[v]', '-map', '[a]',
        '-c:v', 'libx264', '-crf', '23', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k',
        '-movflags', '+faststart', '-t', str(LEN), 'final/Baby-Final-v2.mp4']
subprocess.run(cmd, check=True)
