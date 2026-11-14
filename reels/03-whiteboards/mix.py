"""Efeitos suaves sintetizados (sem IA): troca de cena = sopro curto; toque no fim = sino."""
import numpy as np, scipy.io.wavfile as w
from scipy.signal import butter, sosfilt
sr=44100
D=[2.8,3.0,4.4,4.2,3.6,3.4,3.6,4.2];T=sum(D)
CUTS=np.cumsum(D)[:-1]
rng=np.random.default_rng(7)
def env(n,a,r):
    t=np.arange(n)/sr;return np.minimum(t/a,1)*np.exp(-t/r)
def swipe():
    n=int(sr*.16);air=sosfilt(butter(2,[1800,6500],btype='band',fs=sr,output='sos'),rng.standard_normal(n))*env(n,.012,.045)*.30
    t=np.arange(n)/sr;return air+np.sin(2*np.pi*(520-700*t)*t)*env(n,.002,.03)*.28
def bell(f,d=.55,g=.42):
    n=int(sr*d);t=np.arange(n)/sr;return (np.sin(2*np.pi*f*t)+.35*np.sin(2*np.pi*f*2.01*t))*env(n,.004,.16)*g
def chime(b=1318.5):
    o=np.zeros(int(sr*.8))
    for i,f in enumerate([b,b*1.498]):
        x=bell(f);s=int(sr*.11*i);o[s:s+len(x)]+=x[:len(o)-s]
    return o
buf=np.zeros(int(sr*(T+.5)))
def put(x,t,g=1):
    i=int(t*sr);n=min(len(x),len(buf)-i);buf[i:i+n]+=x[:n]*g
for c in CUTS:put(swipe(),c-.02,.9)
put(chime(),sum(D[:7])+1.0,.8)
buf=buf/max(1,np.abs(buf).max())*.8
w.write('sfx.wav',sr,(buf*32767).astype(np.int16))
