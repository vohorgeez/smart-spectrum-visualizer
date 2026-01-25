import sys
from pyqtgraph.Qt import QtCore, QtWidgets
import numpy as np

from src.ui.spectrum_window import SpectrumWindow
from src.engine import SpectrumEngine

def main():
    app = QtWidgets.QApplication(sys.argv)

    win = SpectrumWindow()
    win.show()

    engine = SpectrumEngine(fs=44100, block=512, n_fft=4096, hop=1024)
    engine.start()

    def tick():
        latest = engine.get_latest()
        if latest is None:
            return
        freqs, db = latest
        win.update_spectrum(freqs, db)

    timer = QtCore.QTimer()
    timer.timeout.connect(tick)
    timer.start(33) # ~30 FPS

    # arrêt propre
    def on_close(event):
        engine.stop()
        event.accept()

    win.closeEvent = on_close

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()