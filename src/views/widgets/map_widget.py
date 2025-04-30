from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene

from src.utils.utils import Clipboard


class MapGraphicsView(QGraphicsView):
    """
    Сцена с картой
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clipboard = Clipboard()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.map_item = None

    def set_map_item(self, map_item: QPixmap):
        """
        Установка карты
        """
        self.scene.removeItem(self.map_item)
        self.scene.addItem(map_item)

    def wheelEvent(self, event) -> None:
        """
        Реализация масштабирования при прокрутке колесика мыши
        """
        scale_factor = 1.5
        factor = scale_factor if event.angleDelta().y() > 0 else 1 / scale_factor
        self.scale(factor, factor)  # Масштабируем как по оси X, так и по оси Y


class MapWidget(QWidget):
    """
    Виджет с картой
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.map_graphics = MapGraphicsView(self)
        self.layout.addWidget(self.map_graphics)
