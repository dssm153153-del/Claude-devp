"""LED 날개 강아지 합본. python3 -I build.py  (work/week3/product4에서 실행)
K1 0–4.2(1x, 걸어오며 올려다봄) → 4.2–7.4(2.5x, 옆으로 도는 구간 압축) → 7.4–9.0(1x, 행인 손 냄새)
→ K2 0.2–5.08(1x, 안아 올려 볼 비빔). 1080x1920 30fps, 상단 자막(원본처럼 고정), 워터마크.
"""
import subprocess
KO = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
CAP1, CAP2 = '밤 산책 나왔다가', '지나가는 사람마다 멈춰섬 ㅋㅋ'
SEG = [('0', 0, 10.08, 2.0), ('1', 0, 5.08, 1.5)]  # v4: 자르지 않고 전체 배속(K1 2배, K2 1.5배), 사이 0.25초 디졸브
V = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1"
txt = lambda s, y: (f"drawtext=fontfile={KO}:text='{s}':fontsize=64:fontcolor=white:borderw=5:bordercolor=black@0.85:x=(w-tw)/2:y={y}")
WM = "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='@pathtorich7':fontsize=36:fontcolor=white@0.55:shadowcolor=black@0.4:shadowx=2:shadowy=2:x=w-tw-40:y=h-110"
parts = [f"[{src}:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{s},{V}[s{i}]" for i, (src, a, b, s) in enumerate(SEG)]
fc = ";".join(parts) + ";" + "".join(f"[s{i}]" for i in range(len(SEG))) + \
     f"xfade=transition=fade:duration=0.25:offset=4.79,{WM},format=yuv420p[v]"
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'clips/K1.mp4', '-i', 'clips/K2.mp4', '-filter_complex', fc,
                '-map', '[v]', '-c:v', 'libx264', '-crf', '17', 'final/Dog-Draft-v5.mp4'], check=True)
print('final/Dog-Draft-v5.mp4')

# 최종: 음악 A1-Music 17.53초부터(0초·4.79초 디졸브가 강박), 0.2초 페이드인·0.8초 페이드아웃
D = 8.2
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'final/Dog-Draft-v5.mp4', '-ss', '17.53', '-i', 'audio/A1-Music.mp3',
                '-filter_complex', f"[1:a]atrim=0:{D},asetpts=PTS-STARTPTS,afade=t=in:d=0.2,afade=t=out:st={D-0.8}:d=0.8,volume=0.9,alimiter=limit=0.9[a]",
                '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', str(D), 'final/Dog-Final-v1.mp4'], check=True)
print('final/Dog-Final-v1.mp4')
