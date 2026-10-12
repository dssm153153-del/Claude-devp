"""Cat-door 합본. python3 -I build.py  (work/week3/cat-door에서 실행)
K1a 0.4–3.4초 1배 → K1a 3.4–5.0초 4배(정지 매달림 압축, K1b 시작 프레임과 이어지게) → K1b 0–4.6초 1배.
1080x1440(3:4) 30fps, 워터마크 @pathtorich7. 무음(효과음은 받으면 추가).
"""
import subprocess
WM = "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='@pathtorich7':fontsize=34:fontcolor=white@0.55:shadowcolor=black@0.35:shadowx=2:shadowy=2:x=w-tw-34:y=34"
V = "scale=1080:1440,fps=30,format=yuv420p"
fc = (f"[0:v]trim=0.4:3.4,setpts=PTS-STARTPTS,{V}[a];"
      f"[0:v]trim=3.4:5.0,setpts=(PTS-STARTPTS)/4,{V}[b];"
      f"[1:v]trim=0:4.6,setpts=PTS-STARTPTS,{V}[c];"
      f"[a][b][c]concat=n=3:v=1:a=0,{WM}[v]")
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'clips/Cat-K1a.mp4', '-i', 'clips/Cat-K1b.mp4',
                '-filter_complex', fc, '-map', '[v]', '-c:v', 'libx264', '-crf', '16', 'final/Cat-Final-v1.mp4'], check=True)
print('final/Cat-Final-v1.mp4')
