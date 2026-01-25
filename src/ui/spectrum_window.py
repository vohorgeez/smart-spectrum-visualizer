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

        self.plot.showGrid(x=True, y=True, alpha=0.2)

        self._log_x = False
        self._fmin = 20.0
        self._fmax = 20000.0

        self.plot.setLabel("left", "Magnitude (dB)")
        self.plot.setLabel("bottom", "Frequency (Hz)")
        self.plot.setYRange(-120, 0)

        self.curve = self.plot.plot(pen=pg.mkPen(width=2))

        self.set_linear_axis()

        toolbar = self.addToolBar("Controls")
        self.log_checkbox = QtWidgets.QCheckBox("Log Freq")
        self.log_checkbox.stateChanged.connect(lambda s: self.set_log_x(s == 2))
        toolbar.addWidget(self.log_checkbox)

    def set_linear_axis(self):
        self.plot.setXRange(self._fmin, self._fmax)
        self.plot.setLabel("bottom", "Frequency (Hz)")
        self.plot.getAxis("bottom").setTicks(None)

    def set_log_axis(self):
        # On affiche X = log10(freq), mais on met des labels en Hz
        self.plot.setXRange(np.log10(self._fmin), np.log10(self._fmax))
        axis = self.plot.getAxis("bottom")
        axis.setLabel("Frequency (Hz)")

        ticks_hz = [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
        ticks = [(np.log10(t), str(t)) for t in ticks_hz]
        axis.setTicks([ticks])

    def set_log_x(self, enabled: bool):
        self._log_x = bool(enabled)
        if self._log_x:
            self.set_log_axis()
        else:
            self.set_linear_axis()

    def update_spectrum(self, freqs: np.ndarray, db: np.ndarray):
        # Sécurité : éviter 0 Hz en log
        freqs = np.asarray(freqs)
        db = np.asarray(db)

        if self._log_x:
            mask = freqs >= self._fmin
            x = np.log10(freqs[mask])
            y = db[mask]
            self.curve.setData(x, y)
        else:
            self.curve.setData(freqs, db)