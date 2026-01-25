# Smart Spectrum Visualizer

Real-time audio spectrum visualizer with FFT and harmonic detection.

## Status
v1 complete

### Features
- Real-time mono audio capture
- Sliding FFT with Hann window
- Overlap processing
- Magnitude spectrum in dB
- Linear / logarithmic frequency display
- Stable real-time performance

### Known limitations (planned for v2)
- UI controls for FFT size and overlap
- Harmonic detection and labeling

## How to run

### Requirements
- Python 3.10+
- A working audio input device (microphone)

### Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/<your-username>/smart-spectrum-visualizer.git
cd smart-spectrum-visualizer
pip install -r requirements.txt
```

### Run the application
From the project root, launch the app as a Python module:
```bash
python -m src.app
```

A window should open displaying a real-time audio spectrum.
The spectrum reacts to ambient sound and supports:
- linear /logarithmic frequency display
- real-time FFT processing with low latency