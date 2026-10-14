"""합성 효과음 + 실내 잡음. python3 -I sfx.py → audio/Cat-SFX.wav (8.03초, 48k 모노)
타이밍(합본 기준): 손잡이 눌림 끝 '딸깍' 2.10초, 손 놓아 손잡이 복귀 '틱' 4.55초, 착지 '툭' 4.95초.
"""
import numpy as np, wave
SR, DUR = 48000, 8.033
rng = np.random.default_rng(7)
t_all = np.arange(int(SR * DUR)) / SR
out = np.zeros_like(t_all)

def pink(n):
    w = rng.standard_normal(n); f = np.fft.rfft(w); f /= np.maximum(1, np.arange(len(f))) ** 0.5
    x = np.fft.irfft(f, n); return x / np.abs(x).max()

def click(freqs, dec, amp):
    n = int(0.12 * SR); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t) for f in freqs) / len(freqs)
    s = s * np.exp(-t / dec) + rng.standard_normal(n) * np.exp(-t / 0.002) * 0.6
    return s * amp

def thud(amp):
    n = int(0.25 * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * (90 - 40 * t / 0.25) * t) * np.exp(-t / 0.05)
    s += np.convolve(rng.standard_normal(n), np.ones(40) / 40, 'same') * np.exp(-t / 0.02) * 2
    return s * amp

def add(sig, at):
    i = int(at * SR); out[i:i + len(sig)] += sig[:len(out) - i]

add(click([2400, 3900, 5200], 0.012, 0.35), 2.06)   # 걸쇠 눌림 1
add(click([1800, 3100], 0.02, 0.45), 2.10)          # 걸쇠 풀림 '딸깍'
add(click([2600, 4100], 0.01, 0.2), 4.55)           # 손잡이 복귀
add(thud(0.6), 4.95)                                # 착지
add(thud(0.15), 5.05)                               # 뒷발
out += pink(len(out)) * 0.004                       # 실내 잡음
out = np.clip(out, -0.95, 0.95)
with wave.open('audio/Cat-SFX.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
print('audio/Cat-SFX.wav')
