"""LED 날개 강아지 합본. python3 -I build.py  (work/week3/product4에서 실행)
K1 0–4.2(1x, 걸어오며 올려다봄) → 4.2–7.4(2.5x, 옆으로 도는 구간 압축) → 7.4–9.0(1x, 행인 손 냄새)
→ K2 0.2–5.08(1x, 안아 올려 볼 비빔). 1080x1920 30fps, 상단 자막(원본처럼 고정), 워터마크.
"""
import subprocess
KO = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
CAP1, CAP2 = '밤 산책 나왔다가', '지나가는 사람마다 멈춰섬 ㅋㅋ'
SEG = [('0', 0.3, 3.6, 1.3), ('0', 7.5, 8.9, 1.3), ('1', 0.5, 2.6, 1.5), ('1', 2.6, 5.08, 1.15)]  # v3: 빠르게(원본 7초 템포)
V = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1"
txt = lambda s, y: (f"drawtext=fontfile={KO}:text='{s}':fontsize=64:fontcolor=white:borderw=5:bordercolor=black@0.85:x=(w-tw)/2:y={y}")
WM = "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='@pathtorich7':fontsize=36:fontcolor=white@0.55:shadowcolor=black@0.4:shadowx=2:shadowy=2:x=w-tw-40:y=h-110"
parts = [f"[{src}:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{s},{V}[s{i}]" for i, (src, a, b, s) in enumerate(SEG)]
fc = ";".join(parts) + ";" + "".join(f"[s{i}]" for i in range(len(SEG))) + \
     f"concat=n={len(SEG)}:v=1:a=0,{txt(CAP1, 230)},{txt(CAP2, 315)},{WM},format=yuv420p[v]"
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'clips/K1.mp4', '-i', 'clips/K2.mp4', '-filter_complex', fc,
                '-map', '[v]', '-c:v', 'libx264', '-crf', '17', 'final/Dog-Draft-v3.mp4'], check=True)
print('final/Dog-Draft-v3.mp4')
