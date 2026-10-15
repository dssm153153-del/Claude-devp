"""마스카라 커플: K1(0–9.7, 앞부분 1.25배속) + K2 + 자막 + 워터마크 (+음악) -> final/Next7-Draft-v1.mp4"""
import subprocess, os, sys
F = '/usr/share/fonts/truetype/nanum/NanumSquareEB.ttf'
MUSIC = sys.argv[1] if len(sys.argv) > 1 else None   # 음악 파일(없으면 무음)
OUT = sys.argv[2] if len(sys.argv) > 2 else 'final/Next7-Final.mp4'
HOLD = 0.3
MOFF = 17.5   # 음악 시작 지점: 음악의 쉼(21.0–22.3)이 '생각' 구간, 22.5 복귀가 면도 시작(5.0초), 끝은 음악 자연 종료
K3 = os.path.exists('clips/Next7-K3.mp4')
# (파일, 시작, 끝, 배속) — 원본 장면 길이에 맞춤(PLAN.md 속도 분석)
SEG = [('clips/Next7-K1.mp4', 0.0, 5.75, 1.64),   # 마스카라 + 남편 따라 하기 (원본 3.5초)
       ('clips/Next7-K1.mp4', 5.75, 8.3, 1.7),    # 눈치채고 생각하는 표정(짧게)
       ('clips/Next7-K1.mp4', 8.3, 9.7, 1.4)]     # 면도 흉내 시작(인중) — 빠르게(사용자)
if K3: SEG.append(('clips/Next7-K3.mp4', 0.0, 4.5, 3.2))  # 볼 면도 — 빠르게(사용자), 약 1.6초
SEG.append(('clips/Next7-K2.mp4', 0.0, 5.167, 1.14))        # 넓은 샷 "나가"(원본 4.5초)
import json
_c = json.load(open('build_k3_color.json'))   # K3 색을 K1에 맞추는 채널별 gain/bias
K3_COLOR = 'lutrgb=' + ':'.join(f"{ch}='clip(val*{g:.4f}+({bb:.2f}),0,255)'" for ch, g, bb in zip('rgb', _c['gain'], _c['bias']))
def _d(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
SEG = [(f, a, b if b is not None else _d(f), s) for f, a, b, s in SEG]
LEN = sum((b - a) / s for _, a, b, s in SEG) + HOLD
SUBS_OFF = [  # (시작, 끝, 화자, 문구)  K2 시작 = 8.4초
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
fc = [f'[{idx[f]}:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{s},' + (K3_COLOR + ',' if 'K3' in f else '') + f'scale=1080:1890,pad=1080:1920:0:15:color=white,fps=30[s{i}]'
      for i, (f, a, b, s) in enumerate(SEG)]
v = ''.join(f'[s{i}]' for i in range(len(SEG))) + f'concat=n={len(SEG)}:v=1:a=0,tpad=stop_mode=clone:stop_duration={HOLD}'
for i, (a, b, who, t) in enumerate([]):  # 자막 없음(사용자 결정)
    p = f'build/sub{i}.txt'; open(p, 'w').write(t)
    y, col = ('150', '#FFE14D') if who == 'him' else ('h*0.80', 'white')
    v += (f",drawtext=fontfile={F}:textfile={p}:fontsize=70:fontcolor={col}:borderw=7:bordercolor=black:"
          f"x=(w-tw)/2:y={y}:enable='between(t,{a},{b})'")
v += f",drawtext=fontfile={F}:text='@pathtorich7':fontsize=38:fontcolor=white@0.6:borderw=1:bordercolor=black@0.3:x=w-tw-36:y=40[v]"
fc.append(v)
if MUSIC:
    cmd += ['-i', MUSIC]
    # 음악 강약(원본 구조: 약 → 정적 → 강 → 컷 전 줄임 → 뽀잉 때 낮춤 → 마무리 강)
    VOL = "if(lt(t,3.3),0.6,if(lt(t,6.9),1.0,if(lt(t,7.4),0.4,if(lt(t,8.35),0.75,1.0))))"
    fc.append(f"[{len(idx)}:a]atrim={MOFF}:{MOFF+LEN},asetpts=PTS-STARTPTS,volume='{VOL}':eval=frame,afade=t=out:st={LEN-0.4}:d=0.4[m]")
    # 원본(audio/Orig.mp3)에서 효과음만 짧게 잘라 장면에 맞춤: (원본 시작, 끝, 원본 정점, 우리 정점, 필터, 볼륨)
    SFX = [(3.15, 3.85, 3.50, 3.45, 'highpass=f=1200', 1.0),   # 휙: 아내가 눈치챔
           (5.10, 5.80, 5.46, 5.05, 'highpass=f=1200', 1.0),   # 휙: 면도 흉내 시작
           (11.65, 12.35, 12.00, 7.45, 'highpass=f=1200', 1.0),  # 휙: 넓은 샷 전환
           ] + ([(5.10, 5.80, 5.46, 8.40, 'highpass=f=1200', 1.0)] if os.environ.get('NAGA', 'whoosh') == 'whoosh' else [])
    # 원본 12.7–13.5 '뽀잉'은 효과음이 아니라 원본 음악의 길게 끄는 음(약 390Hz)이라 우리 음악과 겹치면 어색 → 제외
    oi = len(idx) + 1
    cmd += ['-i', 'audio/Orig.mp3']
    fc.append(f'[{oi}:a]asplit={len(SFX)}' + ''.join(f'[o{i}]' for i in range(len(SFX))))
    for i, (a, b, pk, at, flt, vol) in enumerate(SFX):
        d = int(max(0, at - (pk - a)) * 1000)
        fc.append(f'[o{i}]atrim={a}:{b},asetpts=PTS-STARTPTS,{flt},afade=t=in:d=0.05,afade=t=out:st={b-a-0.15}:d=0.15,volume={vol},adelay={d}:all=1[x{i}]')
    fc.append('[m]' + ''.join(f'[x{i}]' for i in range(len(SFX))) + f'amix=inputs={len(SFX)+1}:normalize=0,atrim=0:{LEN},alimiter=limit=0.89[a]')
else:
    fc.append(f'anoisesrc=color=pink:amplitude=0.0:duration={LEN}[a]')
cmd += ['-filter_complex', ';'.join(fc), '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '23', '-preset', 'slow',
        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', '-t', f'{LEN:.3f}', OUT]
subprocess.run(cmd, check=True)
print(OUT, round(LEN, 2))
