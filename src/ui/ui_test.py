import sys
import numpy as np
from pyqtgraph.Qt import QtCore, QtWidgets
from src.ui.spectrum_window import SpectrumWindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    win = SpectrumWindow()
    win.show()

    # Fake spectrum for testing
    freqs = np.linspace(20, 20000, 1025)
    db = -80 + 10*np.sin(np.linspace(0, 20, len(freqs)))

    def tick():
        # animate a bit
        nonlocal db
        db = np.roll(db, 3)
        win.update_spectrum(freqs, db)

    timer = QtCore.QTimer()
    timer.timeout.connect(tick)
    timer.start(30) # ~33 fps

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()