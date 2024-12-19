from PyQt5.QtWidgets import QMainWindow, QWidget, QGraphicsScene, QGraphicsView, QVBoxLayout


class MapWidget(QGraphicsView):
    """
    Виджет с картой
    """

    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)



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
        self.layout = QVBoxLayout(self.centralwidget)

        self.map_widget = MapWidget()
        self.layout.addWidget(self.map_widget)
