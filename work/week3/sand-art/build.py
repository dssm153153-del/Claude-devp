"""Sand-art 편집. python3 -I build.py  (work/week3/sand-art에서 실행)
원본(알리 판매 영상 1280x720, 24.2초) → 4:5 1080x1350 30fps, 원본 음악 제거, 워터마크.
구간: 회색 대칭 모래줄기 8.70–11.80(훅) → 주황 쏟아짐 0.30–4.80 → 주황 클로즈업 18.25–22.25(17.7–18.2 디졸브 제외).
"""
import subprocess
SEG = [(8.70, 11.80, 760), (0.30, 4.80, 700), (18.25, 22.25, 640)]  # 시작, 끝, 크롭 중심 x
W, H = 576, 720
WM = "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='@pathtorich7':fontsize=38:fontcolor=white@0.6:shadowcolor=black@0.35:shadowx=2:shadowy=2:x=w-tw-36:y=36"
parts, labels = [], []
for i, (a, b, cx) in enumerate(SEG):
    x = max(0, min(1280 - W, cx - W // 2))
    parts.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,crop={W}:{H}:{x}:0,scale=1080:1350:flags=lanczos,fps=30,setsar=1[s{i}]")
    labels.append(f"[s{i}]")
fc = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(SEG)}:v=1:a=0,{WM},format=yuv420p[v]"
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'ref/Src.mp4', '-filter_complex', fc, '-map', '[v]',
                '-c:v', 'libx264', '-crf', '17', 'final/Sand-Draft-v1.mp4'], check=True)
print('final/Sand-Draft-v1.mp4')
