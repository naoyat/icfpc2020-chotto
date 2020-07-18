from scipy.io import wavfile
from scipy import signal
import numpy as np


def find_peak_indices(sxx):
    average = np.average(sxx, axis=1)
    # av = np.average(av1)

    indices = average.argsort()[-2:]
    return sorted(indices)  # lo, hi


def onefreq(sxx, lo, hi, f_unit):
    length = sxx.shape[1]

    cutoff = np.average(sxx[hi+1:, :])
    # print("cutoff = ", cutoff)

    margin = min(4, lo)
    one = np.zeros(length)
    two = np.zeros(length)
    total = 0
    for i in range(length):
        freq = 0
        denom = 0
        for ix in range(lo-margin, hi+margin+1):
            f = ix * f_unit
            v = max(0, sxx[ix,i] - cutoff)
            freq += f * v
            denom += v
        if denom == 0:
            one[i] = 0
            two[i] = 0
        else:
            one[i] = freq / denom
            two[i] = denom
            total += denom

    avg = total / length
    # print("avg=", avg)

    threshold = avg / 5
    for i in range(length):
        if one[i] > 0 and two[i] < threshold:
            one[i] = 0
    return one


def onetwo(of):
    length = len(of)

    out = np.zeros(length, dtype=int)
    m = 50
    for i in range(length):
        if 500-m < of[i] < 500+m:
            out[i] = 1
        elif 600-m < of[i] < 600+m:
            out[i] = 2
        else:
            out[i] = 0
    return out


def rle(of):
    length = len(of)

    res = []
    def flush(last, cnt):
        if last > 0:
            c = round(cnt/9.8)
            return [last-1] * c
        else:
            return []
            # res.append((last-1, c))

    last = -1
    cnt = 0
    for i in range(length):
        if of[i] == last:
            cnt += 1
        else:
            if cnt > 0:
                res += flush(last, cnt)
            last = of[i]
            cnt = 1
    if cnt > 0:
        res += flush(last, cnt)

    return res


def find_width(data):
    L = len(data)
    for i in range(L):
        if data[i] == 0:
            return i-1
    return -1


def reshape(data, width):  #, remove_frame=True):
    L = len(data)
    assert L % width == 0
    # height = (L + width - 1) // width
    height = L // width
    # if width * height > L:
    #     data += [0] * (width * height - L)

    d = np.array(data, dtype=int)
    return d.reshape((height, width))


def read_from_wav(wav_file):
    rate, audio_data = wavfile.read(wav_file)
    f, t, sxx = signal.spectrogram(audio_data, fs=rate, nperseg=256, window='hann')  # nperseg=周波数の分割数=1024 - 44100を1024で割るから44Hz刻みぐらい? ;; 1024だと800ぐらいまで、512にすると1600まで出る

    print("rate=", rate)  # 44100
    print('f:', f.shape)  # (513,) Array of sample frequencies.
    print('t:', t.shape)  # (3041,) Array of segment times.
    print('sxx:', sxx.shape)  # (513, 3041) Spectrogram of x. By default, the last axis of Sxx corresponds to the segment times.

    # seg, length = sxx.shape

    lo, hi = find_peak_indices(sxx)
    # print(lo,hi)
    # mid = (f[lo]+ f[hi])/2
    f_unit = f[1] - f[0]
    of = onefreq(sxx, lo, hi, f_unit)
    # print(of)
    of12 = onetwo(of)
    # print(of12)

    data = rle(of12)
    print('length =', len(data))
    # print(data)
    width = find_width(data)
    print('width =', width)
    data = reshape(data, width)
    # data.reshape((width,))
    return data


def write_to_wav(d, wav_file):
    print('write_to_wav: not supported')
    pass


if __name__ == '__main__':
    d = read_from_wav('radio-transmission-recording.wav')
    print(d.shape)
    print(d)
