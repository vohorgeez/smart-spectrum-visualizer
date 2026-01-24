import numpy as np

def top_peaks(freqs: np.ndarray, db: np.ndarray, k: int = 5,
              fmin: float = 80.0, fmax: float = 5000.0) -> list[tuple[float, float]]:
    """
    Retourne les k pics les plus forts (freq, dB) dans une plage de fréquences.
    Détection simple: on trie par amplitude après masque.
    """
    mask = (freqs >= fmin) & (freqs <= fmax)
    f = freqs[mask]
    d = db[mask]

    if len(d) == 0:
        return []
    
    # un mini-lissage pour éviter de prendre un seul bin au hasard
    if len(d) >= 3:
        d_smooth = (d[:-2] + d[1:-1] + d[2:]) / 3.0
        f_smooth = f[1:-1]
    else:
        d_smooth = d
        f_smooth = f
    
    idx = np.argsort(d_smooth)[-k:][::-1]
    return [(float(f_smooth[i]), float(d_smooth[i])) for i in idx]