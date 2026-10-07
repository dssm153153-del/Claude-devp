"""Final assembly. Usage: python3 -I scripts/build.py <version>  (run from work/video-recreate)

Each segment: (source, start_frame, end_frame_inclusive, speed, xfade_frames_into_this_segment)
Speed >1 = faster. Frames are sampled by nearest source frame (no ghosting).
"""
import subprocess, sys
import cv2
import numpy as np

W, H, FPS = 720, 1280, 30
ZOOM = 1.03  # hides stretched edge strips from the -aligned keyframes

SEGMENTS = [
    # name      file                   start end   speed xfade
    ("K1",   "clips/K1.mp4",       0,  75, 1.6, 0),
    ("K2",   "clips/K2.mp4",      27,  99, 1.3, 0),
    ("K3",   "clips/K3.mp4",       0,  87, 1.8, 0),
    ("K4",   "clips/K4.mp4",       0,  45, 1.6, 0),
    ("K5",   "clips/K5.mp4",      18,  98, 1.6, 0),
    ("K5b",  "clips/K5b.mp4",      1,  48, 1.8, 0),   # bridge: last step, stops behind threshold
    ("K6a",  "clips/K6a.mp4",     12,  38, 1.4, 6),
    ("K6b",  "clips/K6b.mp4",      7,  54, 1.4, 3),
    ("I7",   "images/C7-Insert.png", 0, 0, 1.0, 0),   # 1.8 s still with slow push-in + handheld shake
    ("K8",   "clips/K8.mp4",       0,  84, 1.4, 0),
    ("K9a",  "clips/K9a.mp4",      0,  43, 1.2, 0),
    ("K9b",  "clips/K9b.mp4",      1,  56, 1.15, 0),
    ("K10a1", "clips/K10a.mp4",    0,  24, 3.0, 0),   # step back, fast (keeps seam with K9b continuous)
    ("K10a2", "clips/K10a.mp4",   25,  57, 2.2, 0),   # hands to head
    ("K10b", "clips/K10b-v2.mp4",  6,  50, 1.0, 0),   # fling arms down, storm off
]
TEASER = ("K6a", "K6b", 1.2)   # copy of the climax placed before K1, seconds
INSERT_SEC = 1.8
HOLD_SEC = 1.0
FADE_SEC = 0.4


def fit(img):
    h, w = img.shape[:2]
    s = max(W / w, H / h) * ZOOM
    img = cv2.resize(img, (round(w * s), round(h * s)), interpolation=cv2.INTER_AREA)
    y = (img.shape[0] - H) // 2
    x = (img.shape[1] - W) // 2
    return img[y:y + H, x:x + W]


def read_frames(path):
    cap = cv2.VideoCapture(path)
    out = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        out.append(fit(f))
    return out


def clip_frames(path, a, b, speed):
    src = read_frames(path)[a:b + 1]
    n = max(1, round(len(src) / speed))
    return [src[min(len(src) - 1, round(i * speed))] for i in range(n)]


def insert_frames(path):
    img = cv2.imread(path)
    n = round(INSERT_SEC * FPS)
    rng = np.random.default_rng(7)
    out = []
    for i in range(n):
        t = i / (n - 1)
        z = 1.06 + 0.10 * t
        ang = -6 + 0.6 * np.sin(t * 3.0)
        dx, dy = 2.0 * np.sin(t * 4.1), 2.0 * np.sin(t * 3.3 + 1)
        h, w = img.shape[:2]
        M = cv2.getRotationMatrix2D((w / 2, h / 2), ang, z)
        M[:, 2] += (dx, dy)
        out.append(fit(cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)))
    return out


# Segments whose camera/colour drift from the previous clip: aligned (ECC affine on background)
# and colour-matched (LAB mean/std) to the last frame of REF, for all frames of the group.
CORRECT = {"ref": "K5b", "group": ["K6a", "K6b"]}
MORPH = set()   # seams done with optical-flow morph instead of plain dissolve


def correction(ref, first):
    """Non-rigid background lock: dense flow from ref (last frame of previous clip) to first frame of
    this clip, heavily smoothed, plus LAB colour match. Two independently generated plates differ by
    small local offsets everywhere (door frame, handle, poster lines), which an affine fit cannot fix."""
    dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    fl = dis.calc(cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY), cv2.cvtColor(first, cv2.COLOR_BGR2GRAY), None)
    fl = cv2.GaussianBlur(fl, (0, 0), 8)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    mx, my = xx + fl[..., 0], yy + fl[..., 1]
    warp = lambda im: cv2.remap(im, mx, my, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    la = cv2.cvtColor(ref, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32)
    lb = cv2.cvtColor(warp(first), cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32)
    ma, sa, mb, sb = la.mean(0), la.std(0), lb.mean(0), lb.std(0)

    def apply(im):
        l = cv2.cvtColor(warp(im), cv2.COLOR_BGR2LAB).astype(np.float32)
        l = (l - mb) * (sa / sb) + ma
        return cv2.cvtColor(np.clip(l, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
    return apply


DIS = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)


def morph(a, b, al):
    ga, gb = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY), cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
    fab = DIS.calc(ga, gb, None); fba = DIS.calc(gb, ga, None)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    wa = cv2.remap(a, xx + fba[..., 0] * al, yy + fba[..., 1] * al, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    wb = cv2.remap(b, xx + fab[..., 0] * (1 - al), yy + fab[..., 1] * (1 - al), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return cv2.addWeighted(wa, 1 - al, wb, al, 0)


def main(version):
    built = {}
    stream = []
    for name, path, a, b, sp, xf in SEGMENTS:
        fr = insert_frames(path) if name == "I7" else clip_frames(path, a, b, sp)
        if name == CORRECT["group"][0]:
            fix = correction(built[CORRECT["ref"]][-1], fr[0])
        if name in CORRECT["group"]:
            fr = [fix(f) for f in fr]
        built[name] = fr
        if xf and stream:
            for k in range(xf):
                al = (k + 1) / (xf + 1)
                if name in MORPH:
                    stream[-xf + k] = morph(stream[-xf + k], fr[k], al)
                else:
                    stream[-xf + k] = cv2.addWeighted(stream[-xf + k], 1 - al, fr[k], al, 0)
            fr = fr[xf:]
        if name == TEASER[0]:
            teaser_at = len(stream) - xf
        stream.extend(fr)
    teaser = [f.copy() for f in stream[teaser_at:teaser_at + round(TEASER[2] * FPS)]]
    stream = teaser + stream
    last = stream[-1]
    stream += [last] * round(HOLD_SEC * FPS)
    nf = round(FADE_SEC * FPS)
    for k in range(nf):
        i = len(stream) - nf + k
        stream[i] = (stream[i] * (1 - (k + 1) / nf)).astype(np.uint8)

    out = f"final/Final-v{version}.mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out],
                         stdin=subprocess.PIPE)
    for f in stream:
        p.stdin.write(f.tobytes())
    p.stdin.close()
    p.wait()
    t = 0
    print(f"teaser 0.00-{len(teaser)/FPS:.2f}")
    t = len(teaser)
    for name, *_ in SEGMENTS:
        n = len(built[name]) - (dict((s[0], s[5]) for s in SEGMENTS)[name])
        print(f"{name:5s} {t/FPS:5.2f}-{(t+n)/FPS:5.2f}")
        t += n
    print(f"total {len(stream)/FPS:.2f}s -> {out}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "1")
