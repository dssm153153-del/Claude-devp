"""Coupang product promo video helpers (eunchae-video에서 검증).

python3 -I promo.py slow   <src.mp4> <out.mp4> [target_sec=5.2]
python3 -I promo.py beat   <music.mp3> <cut1,cut2,...>          -> 비트에 맞는 시작 오프셋
python3 -I promo.py peak   <sfx.mp3>                            -> 0.05초 RMS 표(정점 찾기)
python3 -I promo.py build  <config.json> <out.mp4>              -> 합본+오디오+워터마크
config.json 예:
{"clips":[{"file":"clips/K1.mp4","src_len":3.6},{"file":"clips/K2.mp4","src_len":2.13,"crop":"1080:1920:180:0"}],
 "xfade":{"after":1,"dur":0.2,"type":"smoothleft"},
 "final_image":"images/C5.png","hold":1.2,
 "music":{"file":"audio/A1.mp3","offset":12.57,"fade_out":0.7},
 "sfx":[{"file":"audio/A2.mp3","trim":[0,0.45],"at":5.26,"vol":0.7}],
 "watermark":"@id"}
"""
import json, subprocess, sys
import numpy as np

W, H, FPS = 1080, 1920, 30
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
OUT_LEN = 5.167  # MiniMax H3 출력 길이(고정)


def dur(f):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]))


def pcm(f, sr=22050):
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-i', f, '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'])
    return np.frombuffer(raw, np.float32), sr


def slow(src, out, target=5.2):
    f = target / dur(src)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', src, '-vf',
                    f'setpts={f}*PTS,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1',
                    '-an', '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', out], check=True)
    print(out, round(dur(out), 2), 'x', round(f, 2))


def beat(music, cuts):
    x, sr = pcm(music); hop = 512; dt = hop / sr
    fr = [0.0]; prev = None
    for i in range(len(x) // hop - 2):
        s = np.abs(np.fft.rfft(x[i*hop:i*hop+1024] * np.hanning(1024)))
        if prev is not None:
            fr.append(np.maximum(s - prev, 0).sum())
        prev = s
    fr = np.array(fr); fr = (fr - fr.mean()) / fr.std()
    env = lambda t: fr[max(0, int(t/dt)-1):int(t/dt)+2].max() if int(t/dt) < len(fr) else -9
    span = dur(music) - cuts[-1] - 1.5
    best = max((sum(env(o + c) for c in cuts), o) for o in np.arange(0, span, 0.01))
    print('offset', round(best[1], 2))


def peak(sfx):
    x, sr = pcm(sfx, 44100); w = int(0.05 * sr)
    print(' '.join(f'{i*0.05:.2f}:{np.sqrt((x[j:j+w]**2).mean()):.3f}' for i, j in enumerate(range(0, len(x)-w, w))))


def build(cfg_path, out):
    c = json.load(open(cfg_path))
    inp, fc, lens = [], [], []
    for i, k in enumerate(c['clips']):
        sp = dur(k['file']) / k['src_len']
        vf = (f"crop={k['crop']}," if k.get('crop') else '') + f'scale={W}:{H}'
        inp += ['-i', k['file']]
        fc.append(f'[{i}:v]setpts=PTS/{sp},fps={FPS},{vf},setsar=1,format=yuv420p[c{i}]')
        lens.append(k['src_len'])
    n = len(c['clips']); hold = c.get('hold', 1.2)
    inp += ['-loop', '1', '-t', str(hold), '-i', c['final_image']]
    fc.append(f"[{n}:v]scale={W*2}:{H*2},zoompan=z='1+0.04*on/{int(hold*FPS)}':x='iw/2-(iw/zoom/2)':y='0':d=1:s={W}x{H}:fps={FPS},setsar=1,format=yuv420p[c{n}]")
    labels = [f'c{i}' for i in range(n + 1)]
    xf = c.get('xfade')
    if xf:
        a, b = labels[xf['after']], labels[xf['after'] + 1]
        fc.append(f"[{a}][{b}]xfade=transition={xf.get('type','smoothleft')}:duration={xf['dur']}:offset={lens[xf['after']]-xf['dur']:.3f}[xf]")
        labels = labels[:xf['after']] + ['xf'] + labels[xf['after'] + 2:]
    fc.append(''.join(f'[{l}]' for l in labels) + f'concat=n={len(labels)}:v=1:a=0[v0]')
    wm = c.get('watermark')
    fc.append(f"[v0]drawtext=fontfile={FONT}:text='{wm}':fontsize=40:fontcolor=white@0.5:shadowcolor=black@0.25:shadowx=2:shadowy=2:x=w-tw-50:y=70[v]" if wm else '[v0]null[v]')
    total = sum(lens) - (xf['dur'] if xf else 0) + hold
    ai = n + 1; amix = []
    m = c.get('music')
    if m:
        inp += ['-ss', str(m['offset']), '-t', f'{total:.2f}', '-i', m['file']]
        fc.append(f"[{ai}:a]afade=t=in:d=0.05,afade=t=out:st={total-m.get('fade_out',0.7):.2f}:d={m.get('fade_out',0.7)}[m]"); amix.append('[m]'); ai += 1
    for j, s in enumerate(c.get('sfx', [])):
        inp += ['-i', s['file']]; t0, t1 = s['trim']; ms = int(s['at'] * 1000)
        fc.append(f"[{ai}:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS,afade=t=out:st={(t1-t0)*0.66:.2f}:d={(t1-t0)*0.34:.2f},volume={s.get('vol',0.7)},adelay={ms}|{ms}[s{j}]")
        amix.append(f'[s{j}]'); ai += 1
    maps = ['-map', '[v]']
    if amix:
        fc.append(''.join(amix) + f'amix=inputs={len(amix)}:duration=first:normalize=0,alimiter=limit=0.95[a]')
        maps += ['-map', '[a]', '-c:a', 'aac', '-b:a', '192k']
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', *inp, '-filter_complex', ';'.join(fc), *maps,
                    '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-t', f'{total:.2f}', out], check=True)
    print(out, round(dur(out), 2))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'slow': slow(sys.argv[2], sys.argv[3], float(sys.argv[4]) if len(sys.argv) > 4 else 5.2)
    elif cmd == 'beat': beat(sys.argv[2], [float(v) for v in sys.argv[3].split(',')])
    elif cmd == 'peak': peak(sys.argv[2])
    elif cmd == 'build': build(sys.argv[2], sys.argv[3])
