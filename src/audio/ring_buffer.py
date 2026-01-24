import numpy as np
import threading

class RingBuffer:
    def __init__(self, size: int):
        self.size = size
        self.buf = np.zeros(size, dtype=np.float32)
        self.write_pos = 0
        self.lock = threading.Lock()
        self.total_written = 0

    def write(self, x: np.ndarray):
        x = x.astype(np.float32, copy=False)
        n = len(x)
        if n >= self.size:
            x = x[-self.size:]
            n = self.size
        with self.lock:
            end = self.write_pos + n
            if end <= self.size:
                self.buf[self.write_pos:end] = x
            else:
                k = self.size - self.write_pos
                self.buf[self.write_pos:] = x[:k]
                self.buf[:end - self.size] = x[k:]
            self.write_pos = (self.write_pos + n) % self.size
            self.total_written += n

    def read_last(self, n: int) -> np.ndarray:
        n = min(n, self.size)
        with self.lock:
            start = (self.write_pos - n) % self.size
            if start < self.write_pos:
                out = self.buf[start:self.write_pos].copy()
            else:
                out = np.concatenate((self.buf[start:], self.buf[:self.write_pos])).copy()
        return out
    
    def read_latest_since(self, last_total: int) -> tuple[np.ndarray, int]:
        """
        Returns (new_samples, new_total_written).
        If nothing new, returns (empty_array, current_total).
        """
        with self.lock:
            current_total = self.total_written
            delta = current_total - last_total
            if delta <= 0:
                return np.zeros(0, dtype=np.float32), current_total
            
            # clamp: if we missed too much, only return what we still have
            delta = min(delta, self.size)

            # read last 'delta' samples
            start = (self.write_pos - delta) % self.size
            if start < self.write_pos:
                out = self.buf[start:self.write_pos].copy()
            else:
                out = np.concatenate((self.buf[start:], self.buf[:self.write_pos])).copy()

        return out, current_total