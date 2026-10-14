"""원본(알리) 잘라 쓰기 초안. python3 -I build_src.py (work/week3/fruit-picker)
상품과 같은 빨간 바구니 구간만: 0–3.6(사과나무·감 쏙) / 13.83–17.1(헤드 결합) / 17.1–18.0(장대 연결).
중국어 자막 띠(y 870–1010, 720x1280 기준)를 흐림+어둡게 덮고 그 자리에 한국어 자막.
"""
import subprocess
F = '/usr/share/fonts/truetype/nanum/NanumSquareEB.ttf'
SEG = [(0, 1.7, 1.0, '높이 달린 과일 이걸로 쏙'), (15.67, 18.4, 1.2, '손 안 닿는 꼭대기 사과까지'), (13.83, 15.4, 1.3, '장대 이어서 4m까지')]  # v4b: 원속도 이상(느림 지적)
parts = []
for i, (a, b, s, cap) in enumerate(SEG):
    parts.append(f"[0:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{s},split[x{i}][y{i}];"
                 f"[y{i}]crop=720:190:0:870,boxblur=25:2,eq=brightness=-0.25[b{i}];[x{i}][b{i}]overlay=0:870,"
                 f"drawtext=fontfile={F}:text='{cap}':fontsize=52:fontcolor=white:borderw=6:bordercolor=black:x=(w-tw)/2:y=915,"
                 f"scale=1080:1920:flags=lanczos,fps=30,setsar=1[s{i}]")
fc = ";".join(parts) + ";" + "".join(f"[s{i}]" for i in range(len(SEG))) + f"concat=n={len(SEG)}:v=1:a=0,format=yuv420p[v]"
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'ref/Src.mp4', '-filter_complex', fc, '-map', '[v]',
                '-c:v', 'libx264', '-crf', '18', 'final/Src-Cut-Draft-v4.mp4'], check=True)
print('final/Src-Cut-Draft-v4.mp4')
