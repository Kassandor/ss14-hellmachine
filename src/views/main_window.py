from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from src.views.widgets.map_widget import MapWidget


class HMApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hell Machine')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.central_widget = QWidget(self)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        self.map_widget = MapWidget(self)
        self.main_layout.addWidget(self.map_widget)
