import time
import numpy as np
import sounddevice as sd

from audio.ring_buffer import RingBuffer
from dsp.fft import spectrum_db
from dsp.peaks import top_peaks

FS = 44100
BLOCK = 512
N_FFT = 4096

rb = RingBuffer(size=FS * 2)

def audio_callback(indata, frames, time_info, status):
    if status:
        pass
    rb.write(indata[:,0])

with sd.InputStream(channels=1, samplerate=FS, blocksize=BLOCK, callback=audio_callback):
    print("Streaming... (Ctrl+C to stop)")
    while True:
        x = rb.read_last(N_FFT)
        freqs, db = spectrum_db(x, FS)

        # simple "sanity check": print peak frequency
        idx = int(np.argmax(db))
        peaks = top_peaks(freqs, db, k=5, fmin=80.0, fmax=5000.0)
        line = " | ".join([f"{f:6.1f}Hz {a:6.1f}dB" for f, a in peaks])
        print(line)
        time.sleep(0.1)