import numpy as np

def hann_window(n: int) -> np.ndarray:
    return np.hanning(n).astype(np.float32)

def spectrum_db(x: np.ndarray, fs: int) -> tuple[np.ndarray, np.ndarray]:
    """
    x: mono audio samples (1D), length N
    fs: sample rate
    Returns:
        freqs: (N//2 +1,) in Hz
        db: (N//2 +1,) magnitude in dBFS-ish (relative)
    """
    x = x.astype(np.float32, copy=False)
    n = len(x)

    w = hann_window(n)
    xw = x * w

    X = np.fft.rfft(xw)
    mag = np.abs(X)

    eps = 1e-12
    db = 20.0 * np.log10(mag + eps)

    freqs = np.fft.rfftfreq(n, d=1.0 / fs)
    return freqs, db