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

# v1: 음악(A1-Music 11.71초부터, 컷 0/3.1/7.6이 강박에 맞는 오프셋), 0.3초 페이드인·1초 페이드아웃
D = 11.6
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'final/Sand-Draft-v1.mp4', '-ss', '11.71', '-i', 'audio/A1-Music.mp3',
                '-filter_complex', f"[1:a]atrim=0:{D},asetpts=PTS-STARTPTS,afade=t=in:d=0.3,afade=t=out:st={D-1}:d=1,volume=0.9,alimiter=limit=0.9[a]",
                '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', str(D), 'final/Sand-Final-v1.mp4'], check=True)
print('final/Sand-Final-v1.mp4')

# v3(v2 대체): 쿠팡은 검정 테두리만 판매 → 엔드카드를 검정 테두리 사진(Sand-Still-v2-gen.png)으로. 전신이 안 보여서 끝에 GPT 생활 사진(Sand-Still-gen.png) 1.6초 엔드카드(1.08→1.0 줌아웃) 추가, 음악 같은 오프셋으로 13.2초
END = 1.6
D2 = 11.6 + END
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-loop', '1', '-framerate', '30', '-t', str(END), '-i', 'images/Sand-Still-v2-gen.png',
                '-filter_complex', f"[0:v]scale=1080:1350:force_original_aspect_ratio=increase,crop=1080:1350,scale=1166:1458,"
                f"zoompan=z='1.08-0.08*on/{int(END*30)}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1350:fps=30,{WM},format=yuv420p[v]",
                '-map', '[v]', '-c:v', 'libx264', '-crf', '17', '-t', str(END), 'final/endcard.mp4'], check=True)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'final/Sand-Draft-v1.mp4', '-i', 'final/endcard.mp4', '-ss', '11.71', '-i', 'audio/A1-Music.mp3',
                '-filter_complex', f"[0:v][1:v]concat=n=2:v=1:a=0[v];[2:a]atrim=0:{D2},asetpts=PTS-STARTPTS,afade=t=in:d=0.3,afade=t=out:st={D2-1}:d=1,volume=0.9,alimiter=limit=0.9[a]",
                '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '17', '-c:a', 'aac', '-b:a', '192k', '-t', str(D2), 'final/Sand-Final-v3.mp4'], check=True)
print('final/Sand-Final-v3.mp4')
