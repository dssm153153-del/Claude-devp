"""퍼그 야바위 편집. python3 -I build.py (work/week3/dog-shell)
원본 378x480 55초(무음) → 1080x1372(원본 비율) 30fps. 자르지 않고 배속:
0–9초 1.5x(첫 판, 새끼 한 마리 이동) / 9–44초 6x(새끼들이 하나씩 엄마 바구니로) / 44–55초 1.6x(빈 바구니 확인).
자막: 위 고정 2줄, 마지막 구간 결말 자막.
"""
import subprocess
F = '/usr/share/fonts/truetype/nanum/NanumSquareEB.ttf'
def T(s, y, size=78, en=''):
    return f"drawtext=fontfile={F}:text='{s}':fontsize={size}:fontcolor=white:borderw=8:bordercolor=black:x=(w-tw)/2:y={y}" + (f":enable='{en}'" if en else '')
SEG = [(0, 9, 1.2), (9, 44, 3.5), (44, 51.3, 1.3), (51.3, 55.06, 1.0)]  # v3: 마지막 '말리는 앞발'은 원속도
t1 = 9 / 1.2; t2 = t1 + 35 / 3.5; t3 = t2 + 7.3 / 1.3
WM = "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='@pathtorich7':fontsize=32:fontcolor=white@0.6:shadowcolor=black@0.4:shadowx=2:shadowy=2:x=w-tw-30:y=h-80"
parts = [f"[0:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{s},scale=1080:1372:flags=lanczos,fps=30,setsar=1[s{i}]" for i, (a, b, s) in enumerate(SEG)]
fc = ";".join(parts) + ";[s0][s1][s2][s3]concat=n=4:v=1:a=0," + ",".join([
    T('퍼그 엄마랑 야바위 한판', 40), T('판돈은 새끼들 ㄷㄷ', 135),
    T('한 마리씩 엄마한테 넘어가는 중', 1180, 64, f'between(t,{t1:.2f},{t2:.2f})'),
    T('결국 다 털림 ㅋㅋㅋ', 1170, 84, f'between(t,{t2+1:.2f},{t3:.2f})'),
    T('한 마리만 빌려달라니까', 1100, 74, f'gte(t,{t3:.2f})'),
    T('앞발로 바로 컷 ㅋㅋㅋ', 1200, 84, f'gte(t,{t3+1.4:.2f})'), WM]) + ",format=yuv420p[v]"
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'ref/Src.mp4', '-filter_complex', fc, '-map', '[v]',
                '-c:v', 'libx264', '-crf', '18', 'final/Pug-Draft-v3.mp4'], check=True)
print('final/Pug-Draft-v3.mp4')

# 최종: 음악(컷 0/7.5/17.5 강박 오프셋) + 앞발 컷 순간 '삑'(S1-Stop 0–0.7초)
D = 26.866
STOP_AT = t3 + 1.4
OFF = 0.6  # promo.py beat (컷 0/7.5/17.5, 26.9초까지 음악이 남도록)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'final/Pug-Draft-v3.mp4', '-i', 'audio/A1-Music.mp3', '-i', 'audio/S1-Stop.mp3',
                '-filter_complex', f"[1:a]atrim={OFF}:{OFF + D},asetpts=PTS-STARTPTS,afade=t=in:d=0.2,afade=t=out:st={D-1}:d=1,volume=0.8[m];"
                f"[2:a]atrim=0:0.7,asetpts=PTS-STARTPTS,afade=t=out:st=0.5:d=0.2,volume=0.7,adelay={int(STOP_AT*1000)}|{int(STOP_AT*1000)}[s];"
                "[m][s]amix=inputs=2:normalize=0,alimiter=limit=0.9[a]",
                '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', str(D), 'final/Pug-Final-v1.mp4'], check=True)
print('final/Pug-Final-v1.mp4', round(STOP_AT, 2))
