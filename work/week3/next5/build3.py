"""물속 귤 v3. python3 -I build3.py (work/week3/next5)
아이 3명(초록 3.87–8.4 1.8x / 오프로드 15.03–16.73 1.2x / 물 넘침 9.0–11.97 1.15x), 얼굴은 고정 흐림 박스,
문구 카드 1.4초, 직촬 0.5–7.9 1.25x. 자막 NanumSquare ExtraBold 큰 글씨 + 두꺼운 외곽선.
"""
import subprocess
FONT = '/usr/share/fonts/truetype/nanum/NanumSquareEB.ttf'
def T(s, y, size=92): return (f"drawtext=fontfile={FONT}:text='{s}':fontsize={size}:fontcolor=white:"
                             f"borderw=9:bordercolor=black:x=(w-tw)/2:y={y}")
WM = "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='@pathtorich7':fontsize=36:fontcolor=white@0.55:shadowcolor=black@0.4:shadowx=2:shadowy=2:x=w-tw-40:y=h-110"
# (시작, 끝, 배속, 흐림 박스들 x,y,w,h — 원본 720x1280 기준)
KIDS = [
    (3.87, 8.4, 1.8, [(0, 0, 330, 760), (480, 420, 240, 330)]),
    (15.03, 16.73, 1.2, [(380, 0, 340, 300), (20, 380, 200, 230)]),
    (9.0, 11.97, 1.15, [(330, 0, 390, 290), (0, 470, 150, 260)]),
]
fc, labels = [], []
for i, (a, b, s, boxes) in enumerate(KIDS):
    chain = f"[0:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{s},fps=30"
    cur = f"k{i}"
    fc.append(chain + f",split={len(boxes)+1}[{cur}_0]" + "".join(f"[{cur}_b{j}]" for j in range(len(boxes))))
    base = f"{cur}_0"
    for j, (x, y, w, h) in enumerate(boxes):
        fc.append(f"[{cur}_b{j}]crop={w}:{h}:{x}:{y},boxblur=30:3[{cur}_bl{j}]")
        nxt = f"{cur}_o{j}"
        fc.append(f"[{base}][{cur}_bl{j}]overlay={x}:{y}[{nxt}]")
        base = nxt
    fc.append(f"[{base}]scale=1080:1920:flags=lanczos,setsar=1[K{i}]")
    labels.append(f"[K{i}]")
fc.append("".join(labels) + f"concat=n={len(KIDS)}:v=1:a=0," + T('물 한 방울도 안 넘치게', 170) + "," + T('귤 꺼내기 도전', 290) + ",split[A][Alast]")
fc.append("[Alast]reverse,trim=0:0.04,setpts=PTS-STARTPTS,loop=loop=42:size=1:start=0,boxblur=25,eq=brightness=-0.2,"
          + T('애들은 다', 760, 104) + "," + T('물 넘쳐서 실패', 890, 104) + "," + T('그래서 직접 해봄', 1060, 104) + "[B]")
fc.append("[1:v]trim=0.5:7.9,setpts=(PTS-STARTPTS)/1.25,scale=1080:1920:flags=lanczos,fps=30,setsar=1[C]")
fc.append("[A][B][C]concat=n=3:v=1:a=0," + WM + ",format=yuv420p[v]")
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'ref/Src.mp4', '-i', 'ref/My.mp4', '-filter_complex', ";".join(fc),
                '-map', '[v]', '-c:v', 'libx264', '-crf', '17', 'final/Jar-Draft-v3.mp4'], check=True)
print('final/Jar-Draft-v3.mp4')
