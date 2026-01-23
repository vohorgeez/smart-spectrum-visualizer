import time
import numpy as np
import sounddevice as sd

from audio.ring_buffer import RingBuffer
from dsp.fft import spectrum_db

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
        print(f"Peak ~ {freqs[idx]:7.1f} Hz | {db[idx]:6.1f} dB")
        time.sleep(0.1)