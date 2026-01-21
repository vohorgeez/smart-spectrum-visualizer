# Smart Spectrum Visualizer

Real-time audio spectrum visualizer with FFT and harmonic detection.

## v1 goals
- Real-time mono audio capture
- Sliding window FFT (512-4096)
- Hann window
- Magnitude in dB
- Linear / logarithmic frequency display
- Stable real-time behavior (<= 100 ms latency)

## Tech
Python, NumPy, sounddevice