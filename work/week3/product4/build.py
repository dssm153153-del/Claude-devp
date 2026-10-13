"""Dog LED 날개 합본. python3 -I build.py  (work/week3/product4에서 실행)
Dog-K1-v3(720x1280, 10.08초) → 1080x1920 30fps, 워터마크.
속도: 0–4초 2배(멀리서 작은 불빛) → 4–6초 1.4배 → 6–10초 1배(정체 공개). 약 7.4초.
"""
import subprocess
SEG = [(0, 4, 2.0), (4, 6, 1.4), (6, 10.04, 1.0)]
WM = "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='@pathtorich7':fontsize=40:fontcolor=white@0.55:shadowcolor=black@0.35:shadowx=2:shadowy=2:x=w-tw-40:y=60"
parts = [f"[0:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{s},scale=1080:1920:flags=lanczos,fps=30[s{i}]" for i, (a, b, s) in enumerate(SEG)]
fc = ";".join(parts) + ";" + "".join(f"[s{i}]" for i in range(len(SEG))) + f"concat=n={len(SEG)}:v=1:a=0,{WM},format=yuv420p[v]"
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'clips/Dog-K1-v3.mp4', '-filter_complex', fc, '-map', '[v]',
                '-c:v', 'libx264', '-crf', '17', 'final/Dog-Draft-v1.mp4'], check=True)
print('final/Dog-Draft-v1.mp4')
