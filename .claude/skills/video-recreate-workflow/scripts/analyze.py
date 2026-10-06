"""Reference video analysis: timecoded contact sheets, cuts, motion curve, repeated segments.

Usage: python3 -I analyze.py <video> <out_dir> [--fps 5] [--chunk 2]
Outputs in out_dir: info.txt, sheets/tXX.png (every `chunk` seconds, `fps` frames/s with timecode),
report.txt (cuts, 0.5s motion/zoom curve, duplicated segments such as teasers).
"""
import argparse, json, os, subprocess
import cv2
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("out")
ap.add_argument("--fps", type=float, default=5); ap.add_argument("--chunk", type=float, default=2)
ap.add_argument("--width", type=int, default=288)
a = ap.parse_args()
os.makedirs(os.path.join(a.out, "sheets"), exist_ok=True)

probe = json.loads(subprocess.check_output(
    ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", a.video]))
v = next(s for s in probe["streams"] if s["codec_type"] == "video")
dur = float(probe["format"]["duration"])
has_audio = any(s["codec_type"] == "audio" for s in probe["streams"])
with open(os.path.join(a.out, "info.txt"), "w") as f:
    f.write(f"{v['width']}x{v['height']} fps={v['r_frame_rate']} duration={dur:.2f}s audio={has_audio}\n")

# timecoded sheets: one per chunk, 5 columns
n = int(a.fps * a.chunk); rows = int(np.ceil(n / 5))
t = 0.0
while t < dur:
    vf = (f"fps={a.fps},scale={a.width}:-1,"
          "drawtext=text='%{pts\\:hms}':x=8:y=8:fontsize=22:fontcolor=yellow:box=1:boxcolor=black@0.6,"
          f"tile=5x{rows}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t}", "-t", f"{a.chunk}", "-i", a.video,
                    "-copyts", "-vf", vf, "-frames:v", "1",
                    os.path.join(a.out, "sheets", f"t{t:05.1f}.png")], check=True)
    t += a.chunk

# per-frame grayscale thumbnails
cap = cv2.VideoCapture(a.video); fps = cap.get(cv2.CAP_PROP_FPS) or 30
F = []
while True:
    ok, fr = cap.read()
    if not ok: break
    F.append(cv2.cvtColor(cv2.resize(fr, (72, 128)), cv2.COLOR_BGR2GRAY).astype(np.float32))
diff = [0.0] + [float(np.abs(F[i] - F[i - 1]).mean()) for i in range(1, len(F))]

out = []
# cuts: spike well above local motion
med = np.median(diff[1:])
cuts = [i for i in range(1, len(F)) if diff[i] > max(25, 6 * med)]
out.append("CUTS: " + ", ".join(f"{i / fps:.2f}s(d={diff[i]:.0f})" for i in cuts))
bounds = [0] + cuts + [len(F)]
out.append("SHOTS: " + ", ".join(f"[{bounds[k] / fps:.2f}-{bounds[k + 1] / fps:.2f}]" for k in range(len(bounds) - 1)))

# 0.5s motion + zoom curve (ECC affine, within shots only)
out.append("\nTIME  MOTION  ZOOM")
step = int(fps / 2)
for s in range(0, len(F), step):
    ms = diff[s:s + step]; zs = []
    for i in range(max(s, 1), min(s + step, len(F))):
        if i in cuts: continue
        try:
            w = np.eye(2, 3, dtype=np.float32)
            _, w = cv2.findTransformECC(F[i - 1], F[i], w, cv2.MOTION_AFFINE,
                                        (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 1e-4), None, 5)
            zs.append((abs(w[0, 0]) + abs(w[1, 1])) / 2)
        except cv2.error:
            pass
    out.append(f"{s / fps:5.1f}s {np.mean(ms):6.2f}  {np.mean(zs) if zs else float('nan'):.4f}")

# duplicated segments (teaser / replay): each shot's first frames vs. all other shots
out.append("\nREPEATS (shot start matched elsewhere, diff<8):")
for k in range(len(bounds) - 1):
    i = bounds[k]
    cand = [(float(np.abs(F[i] - F[j]).mean()), j) for j in range(len(F)) if not (bounds[k] <= j < bounds[k + 1])]
    d, j = min(cand)
    if d < 8:
        L = bounds[k + 1] - bounds[k]
        out.append(f"shot {bounds[k] / fps:.2f}-{bounds[k + 1] / fps:.2f}s == {j / fps:.2f}-{(j + L) / fps:.2f}s (diff {d:.1f})")

with open(os.path.join(a.out, "report.txt"), "w") as f:
    f.write("\n".join(out) + "\n")
print("\n".join(out))
