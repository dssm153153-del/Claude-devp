"""v4: 원본 소리(audio/Orig.mp3 2.4~14.4초)를 그대로 깔고, K1 영상을 소리 타이밍에 맞춰 구간별 속도 조절."""
import subprocess, os
F = '/usr/share/fonts/truetype/nanum/NanumSquareEB.ttf'
A0, A1 = 2.4, 14.4            # 원본 소리 구간
# (K1 시작, K1 끝, 원본 소리 시작, 원본 소리 끝)
MAP = [(0.0, 2.2, 2.4, 4.75),   # 엄마 "give me my baby back"
       (2.2, 2.5, 4.75, 5.1),   # 거절① 고개 휙 = 원본 흔들기 소리
       (2.5, 4.5, 5.1, 8.1),    # 응시 + "Jake buddy he is my baby"
       (4.5, 6.7, 8.1, 9.6),    # 거절② 고개 젖힘 = 아기 웃음
       (6.7, 10.125, 9.6, 13.2)]  # 다시 안기 + "Jake he's my baby"
HOLD = A1 - MAP[-1][3]         # 마지막 프레임 정지(아기 웃음 13.5~14.3 구간)
LEN = A1 - A0
SUBS = [(0.3, 2.35, 'mom', '엄마: 제이크, 내 아기 돌려줘'),
        (2.35, 3.0, 'mom', '엄마: 제이크, 내 아기 돌려줘'),
        (2.35, 3.0, 'jake', '제이크: 싫어'),
        (3.0, 5.7, 'mom', '엄마: 제이크… 걔는 내 아기야'),
        (5.7, 7.4, 'mom', '엄마: 제이크… 걔는 내 아기야'),
        (5.7, 7.4, 'jake', '제이크: 싫다니까!!'),
        (9.0, LEN, 'mom', '엄마: 내 아기라고!!'),
        (10.8, LEN, 'jake', '제이크: (못 들은 척 꼭 안음)')]
os.makedirs('build', exist_ok=True)
parts = []
for i, (k0, k1, a0, a1) in enumerate(MAP):
    f = (a1 - a0) / (k1 - k0)
    parts.append(f'[0:v]trim={k0}:{k1},setpts=(PTS-STARTPTS)*{f:.4f}[p{i}]')
vf = parts + [''.join(f'[p{i}]' for i in range(len(MAP))) + f'concat=n={len(MAP)}:v=1:a=0,'
              f'scale=1097:1920,crop=1080:1920,fps=30,tpad=stop_mode=clone:stop_duration={HOLD}']
draw = []
for i, (a, b, who, t) in enumerate(SUBS):
    p = f'build/sub{i}.txt'; open(p, 'w').write(t)
    y, col = ('h*0.80', 'white') if who == 'mom' else ('150', '#FFE14D')
    draw.append(f"drawtext=fontfile={F}:textfile={p}:fontsize=70:fontcolor={col}:borderw=7:bordercolor=black:"
                f"x=(w-tw)/2:y={y}:enable='between(t,{a},{b})'")
draw.append(f"drawtext=fontfile={F}:text='@pathtorich7':fontsize=38:fontcolor=white@0.5:x=w-tw-36:y=40[v]")
vf[-1] += ',' + ','.join(draw)
# 원본 13.2~13.5 흔들기 소리(영상엔 흔들기 없음)는 줄임
af = (f"[1:a]atrim={A0}:{A1},asetpts=PTS-STARTPTS,"
      f"volume='if(between(t,{13.2-A0},{13.5-A0}),0.25,1)':eval=frame,afade=t=out:st={LEN-0.4}:d=0.4[a]")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'clips/Baby-K1.mp4', '-i', 'audio/Orig.mp3',
                '-filter_complex', ';'.join(vf) + ';' + af, '-map', '[v]', '-map', '[a]',
                '-c:v', 'libx264', '-crf', '23', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k',
                '-movflags', '+faststart', '-t', f'{LEN}', 'final/Baby-Final-v4.mp4'], check=True)
