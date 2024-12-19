from PyQt5.QtWidgets import QMainWindow, QWidget


class HMApp(QMainWindow):
    """
    Основное окно
    Орбитальная система наведения HellMachine
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle('HellMachine')
        self.setGeometry(100, 100, 800, 600)
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
