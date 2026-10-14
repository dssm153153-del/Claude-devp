"""Final assembly for eunchae-video. Run: python3 scripts/build.py [version]"""
import subprocess, sys
v = sys.argv[1] if len(sys.argv) > 1 else '1'
W, H, FPS = 1080, 1920, 30
# (file, speed, video filter to reach WxH)
clips = [
    ('clips/K1-v2.mp4', 1.43, f'scale={W}:{H}'),                       # covers source 0-3.6s
    ('clips/K2-v2.mp4', 2.42, f'crop=1080:1920:180:0,scale={W}:{H}'),  # source 4.13-6.25 (3:4 -> center crop)
    ('clips/K4.mp4',    1.69, f'scale={W}:{H}'),                       # source 8.11-11.16
]
C5_HOLD = 1.2
XF = 0.2  # K2 -> K4 smooth slide (stands in for skipped K3 fling)
inp, fc = [], []
for i, (f, s, vf) in enumerate(clips):
    inp += ['-i', f]
    fc.append(f'[{i}:v]setpts=PTS/{s},fps={FPS},{vf},setsar=1,format=yuv420p[c{i}]')
n = len(clips)
inp += ['-loop', '1', '-t', str(C5_HOLD), '-i', 'images/C5.png']
fc.append(f"[{n}:v]scale={W*2}:{H*2},zoompan=z='1+0.04*on/{int(C5_HOLD*FPS)}':x='iw/2-(iw/zoom/2)':y='0':d=1:s={W}x{H}:fps={FPS},setsar=1,format=yuv420p[c5]")
def dur(f, s):
    d = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
    return d / s
d1 = dur(*clips[1][:2])
fc.append(f'[c1][c2]xfade=transition=smoothleft:duration={XF}:offset={d1-XF:.3f}[c12]')
fc.append('[c0][c12][c5]concat=n=3:v=1:a=0[v]')
out = f'final/Final-v{v}.mp4'
subprocess.run(['ffmpeg','-loglevel','error','-y',*inp,'-filter_complex',';'.join(fc),'-map','[v]','-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-r',str(FPS),out], check=True)
print(out)
