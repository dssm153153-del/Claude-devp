"""물속 귤 편집. python3 -I build.py (work/week3/next5에서 실행)
도전 장면 1개(9.00–11.97, 물 넘침이 보이는 시도, 1x) + 결말 전체(16.73–34.27, 손가락 하나로 귤이 따라 올라옴, 1.8x).
원본 소리 제거, 1080x1920 30fps, 워터마크.
"""
import subprocess
SEG = [(9.00, 11.97, 1.0), (16.73, 34.27, 1.8)]
WM = "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='@pathtorich7':fontsize=36:fontcolor=white@0.55:shadowcolor=black@0.4:shadowx=2:shadowy=2:x=w-tw-40:y=60"
parts = [f"[0:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{s},scale=1080:1920:flags=lanczos,fps=30,setsar=1[s{i}]" for i, (a, b, s) in enumerate(SEG)]
fc = ";".join(parts) + ";[s0][s1]concat=n=2:v=1:a=0," + WM + ",format=yuv420p[v]"
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'ref/Src.mp4', '-filter_complex', fc, '-map', '[v]',
                '-c:v', 'libx264', '-crf', '17', 'final/Jar-Draft-v1.mp4'], check=True)
print('final/Jar-Draft-v1.mp4')
