"""물속 귤 v2. python3 -I build2.py (work/week3/next5)
① 원본 아이 도전(9.00–11.97, 물 넘침) — 얼굴 빼고 크롭(위 190px 제거), 왼쪽 뒤 아이 흐림, 자막 "물 한 방울도 안 넘치게 귤 꺼내기"
② 문구 카드 1.3초 "애들은 다 실패… / 그래서 직접 해봄" (①의 마지막 프레임 흐림 배경)
③ 직촬(My.mp4 0.5–7.9, 1.25x): 손가락으로 물만 살살 → 귤이 떠오름 → 꺼냄
1080x1920 30fps, 원본 소리 제거, 워터마크.
"""
import subprocess
KO = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
def T(s, y, size=64): return f"drawtext=fontfile={KO}:text='{s}':fontsize={size}:fontcolor=white:borderw=5:bordercolor=black@0.85:x=(w-tw)/2:y={y}"
WM = "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='@pathtorich7':fontsize=36:fontcolor=white@0.55:shadowcolor=black@0.4:shadowx=2:shadowy=2:x=w-tw-40:y=h-110"
fc = (
 "[0:v]trim=9.0:11.97,setpts=PTS-STARTPTS,crop=612:1090:0:190,split[k][kb];"
 "[kb]crop=140:260:0:310,boxblur=20[blr];[k][blr]overlay=0:310,scale=1080:1920:flags=lanczos,fps=30,setsar=1,"
 + T('물 한 방울도 안 넘치게', 200) + "," + T('귤 꺼내기 도전', 285) + ",split[a][alast];"
 "[alast]trim=start=2.9,setpts=PTS-STARTPTS,loop=loop=-1:size=1:start=0,trim=0:1.3,boxblur=25,eq=brightness=-0.15,"
 + T('애들은 다 물 넘쳐서 실패', 820, 70) + "," + T('그래서 직접 해봄', 920, 70) + "[b];"
 "[1:v]trim=0.5:7.9,setpts=(PTS-STARTPTS)/1.25,scale=1080:1920:flags=lanczos,fps=30,setsar=1[c];"
 "[a][b][c]concat=n=3:v=1:a=0," + WM + ",format=yuv420p[v]")
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'ref/Src.mp4', '-i', 'ref/My.mp4', '-filter_complex', fc,
                '-map', '[v]', '-c:v', 'libx264', '-crf', '17', 'final/Jar-Draft-v2.mp4'], check=True)
print('final/Jar-Draft-v2.mp4')
