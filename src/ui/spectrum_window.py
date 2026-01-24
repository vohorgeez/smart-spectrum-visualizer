import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets
import numpy as np

class SpectrumWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Spectrum Visualizer (v1)")
        self.resize(1000, 600)

        self.plot = pg.PlotWidget()
        self.setCentralWidget(self.plot)

        self.plot.setLabel("left", "Magnitude (dB)")
        self.plot.setLabel("bottom", "Frequency (Hz)")
        self.plot.showGrid(x=True, y=True, alpha=0.2)

        self.curve = self.plot.plot(pen=pg.mkPen(width=2))
        self.plot.setXRange(20, 20000)
        self.plot.setYRange(-120, 0)

    def update_spectrum(self, freqs: np.ndarray, db: np.ndarray):
        self.curve.setData(freqs, db)