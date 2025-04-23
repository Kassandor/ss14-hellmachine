import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from frontend.ui import HMApp


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = HMApp()
    main_window.setWindowFlags(main_window.windowFlags() | Qt.WindowStaysOnTopHint)
    main_window.show()

    sys.exit(app.exec_())
