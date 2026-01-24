import numpy as np
from .fft import spectrum_db

class SlidingFFT:
    def __init__(self, fs: int, n_fft: int, hop: int):
        assert hop > 0 and hop <= n_fft
        self.fs = fs
        self.n_fft = n_fft
        self.hop = hop
        self._acc = np.zeros(0, dtype=np.float32)
        self._last_emitted_samples = 0

    def push(self, x: np.ndarray) -> list[tuple[np.ndarray, np.ndarray]]:
        """
        Push new mono samples.
        Returns a list of (freqs, db) frames produces (0, 1, or more)
        """
        x = x.astype(np.float32, copy=False)
        self._acc = np.concatenate([self._acc, x])

        out = []
        # Tant qu'on a au moins n_fft samples, on peut calculer
        while len(self._acc) >= self.n_fft:
            frame = self._acc[:self.n_fft]
            freqs, db = spectrum_db(frame, self.fs)
            out.append((freqs, db))

            # On avance de hop samples (overlap = n_fft - hop)
            self._acc = self._acc[self.hop:]

        return out