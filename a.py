from scipy.io import wavfile
from scipy import signal
import matplotlib.pyplot as plt

rate, data = wavfile.read('radio-transmission-recording.wav')
f, t, sxx = signal.spectrogram(data, fs=rate, nperseg=1024, window='hann')
print(t.shape)
print(f.shape)
print(sxx.shape)

print(t)
print('---')
print(f[:20])
print('---')
print(sxx[:20])

#plt.figure(figsize=(100, 2))
#plt.pcolormesh(t, f[:20], sxx[:20,:], shading='gouraud')
#plt.show()

