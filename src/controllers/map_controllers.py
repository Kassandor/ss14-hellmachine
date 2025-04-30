from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem

from src.models.map import MapsData
from src.views.widgets.map_widget import MapGraphicsView


class MapGraphicsViewController:
    def __init__(self, view: MapGraphicsView, model: MapsData):
        self.view = view
        self.model = model

    def load_map(self, map_name: str):
        """
        Загрузка карты и установка в виджет
        """
        pixmap = QPixmap(self.model.get_map_url(map_name))
        map_item = QGraphicsPixmapItem(pixmap)
        self.view.set_map_item(map_item)
