"""Strandbeest 최종본. python3 -I build.py  (work/week3/strandbeest에서 실행)
SB-K1(2560x1440, 11.54초) → 1920x1080 30fps, 워터마크 오른쪽 위.
오디오: 모델 자체 오디오 버리고 S1-Wind.mp3 0.3초부터, 0.3초 페이드인·0.6초 페이드아웃.
"""
import subprocess
D = 11.5
WM = "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='@pathtorich7':fontsize=36:fontcolor=white@0.6:shadowcolor=black@0.35:shadowx=2:shadowy=2:x=w-tw-40:y=36"
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'clips/SB-K1.mp4', '-ss', '0.3', '-i', 'audio/S1-Wind.mp3',
                '-filter_complex', f"[0:v]scale=1920:1080:flags=lanczos,fps=30,{WM},format=yuv420p[v];"
                f"[1:a]atrim=0:{D},asetpts=PTS-STARTPTS,afade=t=in:d=0.3,afade=t=out:st={D-0.6}:d=0.6,alimiter=limit=0.9[a]",
                '-map', '[v]', '-map', '[a]', '-t', str(D), '-c:v', 'libx264', '-crf', '17', '-c:a', 'aac', '-b:a', '192k',
                'final/SB-Final-v1.mp4'], check=True)
print('final/SB-Final-v1.mp4')
