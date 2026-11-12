"""Mixa trilha + efeitos suaves para o Reel do Habblaud v2.
Efeitos sintetizados aqui (sem IA): troca de cena = 'tick' curto com brilho; permissao e fim = sino suave."""
import numpy as np, scipy.io.wavfile as w
from scipy.signal import butter, sosfilt

D = '/home/claude/urlan-posts/reels/02-habblaud/v2/'
sr = 44100
T = 16.2
CUTS = [2.4, 4.6, 7.0, 9.6, 11.6, 13.8]
rng = np.random.default_rng(7)


def env(n, a, r):
    t = np.arange(n) / sr
    return np.minimum(t / a, 1.0) * np.exp(-t / r)


def swipe():
    """Troca de cena: sopro filtrado muito curto + toque grave leve. ~0.16 s."""
    n = int(sr * 0.16)
    noise = rng.standard_normal(n)
    sos = butter(2, [1800, 6500], btype='band', fs=sr, output='sos')
    air = sosfilt(sos, noise) * env(n, 0.012, 0.045) * 0.30
    t = np.arange(n) / sr
    tone = np.sin(2 * np.pi * (520 - 700 * t) * t) * env(n, 0.002, 0.03) * 0.28
    return air + tone


def bell(freq, dur=0.5, g=0.5):
    n = int(sr * dur)
    t = np.arange(n) / sr
    x = (np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * freq * 2.01 * t)) * env(n, 0.004, 0.16)
    return x * g


def chime(base=1318.5):
    """Dois tons ascendentes (E6 -> B6)."""
    out = np.zeros(int(sr * 0.8))
    for i, f in enumerate([base, base * 1.498]):
        b = bell(f, 0.55, 0.42)
        s = int(sr * 0.11 * i)
        out[s:s + len(b)] += b[:len(out) - s]
    return out


sfx = np.zeros(int(sr * T))
events = []


def put(buf, x, t, g=1.0):
    i = int(max(0, t) * sr)
    x = x * g
    n = min(len(x), len(buf) - i)
    buf[i:i + n] += x[:n]


for c in CUTS:
    put(sfx, swipe(), c - 0.02, 0.9)
    events.append((c - 0.02, 0.3))
put(sfx, chime(), 7.25, 0.9)
events.append((7.25, 0.7))
put(sfx, chime(1046.5), 13.85, 0.75)
events.append((13.85, 0.8))

# trilha
sr_m, m = w.read(D + 'musica.wav')
assert sr_m == sr
m = m.astype(np.float64) / 32768
if m.ndim == 1:
    m = np.stack([m, m], 1)
n = int(sr * T)
m = m[:n]
t = np.arange(len(m)) / sr
fade_in = np.minimum(t / 0.4, 1.0)
fade_out = np.minimum((T - t) / 1.6, 1.0)
gain = 0.50 * fade_in * fade_out
# duck sob os efeitos
duck = np.ones(len(m))
for s, d in events:
    i0, i1 = int(s * sr), int((s + d) * sr)
    ramp = np.ones(len(duck))
    duck[i0:i1] = np.minimum(duck[i0:i1], 0.55)
# suaviza o duck
k = int(sr * 0.05)
duck = np.convolve(duck, np.ones(k) / k, mode='same')
m = m * (gain * duck)[:, None]

out = m + np.stack([sfx, sfx], 1)
peak = np.abs(out).max()
out = out / peak * 0.89
w.write(D + 'mix.wav', sr, (out * 32767).astype(np.int16))
print('pico antes', round(float(peak), 3))
