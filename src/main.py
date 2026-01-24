import time
import numpy as np
import sounddevice as sd

from audio.ring_buffer import RingBuffer
from dsp.sliding_fft import SlidingFFT
from dsp.peaks import top_peaks

FS = 44100
BLOCK = 512
N_FFT = 4096
HOP = 1024 # 75% overlap

rb = RingBuffer(size=FS * 2)
sl = SlidingFFT(fs=FS, n_fft=N_FFT, hop=HOP)

def audio_callback(indata, frames, time_info, status):
    if status:
        pass
    rb.write(indata[:, 0])

last_total = 0

with sd.InputStream(channels=1, samplerate=FS, blocksize=BLOCK, callback=audio_callback):
    print("Streaming... (Ctrl+C to stop)")
    while True:
        new_samples, last_total = rb.read_latest_since(last_total)
        frames = sl.push(new_samples)

        if frames:
            freqs, db = frames[-1]
            peaks = top_peaks(freqs, db, k=5, fmin=80.0, fmax=5000.0)
            line = " | ".join([f"{f:6.1f}Hz {a:6.1f}dB" for f, a in peaks])
            print(line)

        time.sleep(0.01)