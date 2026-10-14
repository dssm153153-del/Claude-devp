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

# v3: 실제 효과음(Freepik) 정점 맞춤 + 옅은 실내 잡음
# S1-Latch: 2.20–2.40(큰 딸깍, 정점 2.26) → 2.10초 / 0.00–0.15(작은 딸깍, 정점 0.07) → 손잡이 복귀 4.55초
# S2-Land: 0.00–0.30(툭+뒷발, 정점 0.02) → 착지 4.95초
D = 8.0
fa = (f"anoisesrc=color=pink:amplitude=0.006:duration={D}[n];"
      "[1:a]atrim=2.20:2.40,asetpts=PTS-STARTPTS,volume=1.0,adelay=2040|2040[l1];"
      "[1:a]atrim=0:0.15,asetpts=PTS-STARTPTS,volume=0.5,adelay=4480|4480[l2];"
      "[2:a]atrim=0:0.30,asetpts=PTS-STARTPTS,volume=1.3,adelay=4930|4930[t];"
      "[n][l1][l2][t]amix=inputs=4:normalize=0,alimiter=limit=0.9,aformat=channel_layouts=stereo[a]")
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'final/Cat-Final-v1.mp4', '-i', 'audio/S1-Latch.mp3', '-i', 'audio/S2-Land.mp3',
                '-filter_complex', fa, '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', str(D),
                'final/Cat-Final-v3.mp4'], check=True)
print('final/Cat-Final-v3.mp4')
