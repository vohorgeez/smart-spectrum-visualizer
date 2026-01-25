import threading
import time
import numpy as np
import sounddevice as sd

from src.audio.ring_buffer import RingBuffer
from src.dsp.sliding_fft import SlidingFFT

class SpectrumEngine:
    def __init__(self, fs: int = 44100, block: int = 512, n_fft: int = 4096, hop: int = 1024):
        self.fs = fs
        self.block = block
        self.n_fft = n_fft
        self.hop = hop

        self.rb = RingBuffer(size=fs * 2)
        self.sl = SlidingFFT(fs=fs, n_fft=n_fft, hop=hop)

        self._last_total = 0
        self._latest = None # tuple(freqs, db)
        self._latest_lock = threading.Lock()

        self._stop = threading.Event()
        self._thread = None
        self._stream = None

    def _audio_callback(self, indata, frames, time_info, status):
        if status:
            pass
        self.rb.write(indata[:, 0])

    def start(self):
        self._stop.clear()
        self._stream = sd.InputStream(
            channels=1,
            samplerate=self.fs,
            blocksize=self.block,
            callback=self._audio_callback
        )
        self._stream.start()

        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=1.0)
        if self._stream:
            self._stream.stop()
            self._stream.close()

    def _run(self):
        while not self._stop.is_set():
            new_samples, self._last_total = self.rb.read_latest_since(self._last_total)
            frames = self.sl.push(new_samples)

            if frames:
                freqs, db = frames[-1]
                with self._latest_lock:
                    self._latest = (freqs, db)

            time.sleep(0.005)

    def get_latest(self):
        with self._latest_lock:
            if self._latest is None:
                return None
            freqs, db = self._latest
            return freqs, db