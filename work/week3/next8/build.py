"""아빠 vs 엄마 무릎베개: 아빠 클립 + 엄마 0–2.5 + 밀어내기(Kling 앞부분) -> final/Next8-Draft-v1.mp4 (무음, 자막 없음)"""
import subprocess
F = '/usr/share/fonts/truetype/nanum/NanumSquareEB.ttf'
SEG = [('clips/Next8-Dad.mp4', 0.0, 9.417, 1.0),      # 아빠: 뽀뽀 2번 + 쓰다듬기 + 꼭 안기
       ('clips/Next8-Mom.mp4', 0.0, 2.5, 1.0),        # 엄마 눕기 → 시큰둥
       ('clips/Next8-Mom-Push.mp4', 0.0, 2.25, 1.0)]  # 한 손으로 툭 밀기(뒷부분은 머리 납작해짐 → 사용 안 함)
HOLD = 0.4
cmd = ['ffmpeg', '-v', 'error', '-y']
for f, *_ in SEG: cmd += ['-i', f]
fc = [f'[{i}:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{s},scale=1080:1080:flags=lanczos,setsar=1,fps=30[s{i}]' for i, (f, a, b, s) in enumerate(SEG)]
fc.append(''.join(f'[s{i}]' for i in range(len(SEG))) + f'concat=n={len(SEG)}:v=1:a=0,tpad=stop_mode=clone:stop_duration={HOLD},'
          f"drawtext=fontfile={F}:text='@pathtorich7':fontsize=34:fontcolor=white@0.6:borderw=1:bordercolor=black@0.3:x=w-tw-30:y=30[v]")
cmd += ['-filter_complex', ';'.join(fc), '-map', '[v]', '-c:v', 'libx264', '-crf', '23', '-preset', 'slow', '-pix_fmt', 'yuv420p',
        '-movflags', '+faststart', 'final/Next8-Draft-v1.mp4']
subprocess.run(cmd, check=True)
