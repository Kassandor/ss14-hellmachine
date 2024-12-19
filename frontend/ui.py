import math
import os

import pyperclip
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPen
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QGraphicsScene,
    QGraphicsView,
    QVBoxLayout,
    QGraphicsPixmapItem,
    QGraphicsLineItem,
    QComboBox,
    QLabel,
    QGraphicsEllipseItem,
)

from backend.maps_data import MapsData
from backend.utils import get_next_fire_time
from base.settings import config


class MapWidget(QGraphicsView):
    """
    Виджет с картой
    """

    def __init__(self, label, map_path):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.map_pixmap = QPixmap(map_path)
        self.map_item = QGraphicsPixmapItem(self.map_pixmap)
        self.scene.addItem(self.map_item)

        self.elem_qty_x, self.elem_qty_y = self.calculate_elem_qty()
        self.grid_step_x, self.grid_step_y = self.calculate_grid_step()

        self.draw_grid()

        self.label = label

        self.dx = 0
        self.dy = 0

        # Атрибут для хранения текущей подсветки
        self.current_highlight = None

    def wheelEvent(self, event):
        """
        Реализация масштабирования при прокрутке колесика мыши
        """
        scale_factor = 1.5
        factor = scale_factor if event.angleDelta().y() > 0 else 1 / scale_factor
        self.scale(factor, factor)  # Масштабируем как по оси X, так и по оси Y

    def mousePressEvent(self, event):
        """
        Логика нажатия кнопки мыши
        """
        if event.button() == Qt.RightButton:
            click_pos = self.mapToScene(event.pos())

            # Переводим координаты Y так, чтобы Y рос вверх
            grid_x, grid_y = (
                math.ceil((click_pos.x() / self.grid_step_x) + self.dx),
                math.ceil(((self.map_pixmap.height() - click_pos.y()) / self.grid_step_y) + self.dy),
            )
            # Обновляем текст в QLabel
            self.label.setText(
                f"Координаты на сетке: X={grid_x}, Y={grid_y}, следующий выстрел в {get_next_fire_time()}"
            )
            pyperclip.copy(f'{grid_x}, {grid_y}')

            # Удаляем предыдущую подсветку (если есть)
            if self.current_highlight:
                self.scene.removeItem(self.current_highlight)

            # Создаем новый элемент подсветки
            highlight_radius = 15  # Радиус подсветки
            highlight = QGraphicsEllipseItem(
                click_pos.x() - highlight_radius,  # x
                click_pos.y() - highlight_radius,  # y
                highlight_radius * 2,  # ширина
                highlight_radius * 2,  # высота
            )
            highlight.setBrush(Qt.red)  # Цвет подсветки (красный)
            # Без обводки
            self.scene.addItem(highlight)

            # Сохраняем текущую подсветку для последующего удаления
            self.current_highlight = highlight
        super().mousePressEvent(event)

    def draw_grid(self):
        """
        Отрисовка координатной сетки
        """
        pen = QPen(Qt.red)
        pen.setStyle(Qt.DashLine)
        pen.setWidth(1)
        self.draw_x(pen)
        self.draw_y(pen)

    def draw_x(self, pen):
        """
        Отрисовка X-горизонтали
        """
        for x in range(0, self.map_pixmap.width(), self.grid_step_x):
            line_item = QGraphicsLineItem(x, 0, x, self.map_pixmap.height())  # (x1, y1, x2, y2)
            line_item.setPen(pen)
            self.scene.addItem(line_item)

    def draw_y(self, pen):
        """
        Отрисовка Y-вертикали
        """
        for y in range(0, self.map_pixmap.height(), self.grid_step_y):
            line_item = QGraphicsLineItem(0, y, self.map_pixmap.width(), y)  # (x1, y1, x2, y2)
            line_item.setPen(pen)
            self.scene.addItem(line_item)

    def calculate_elem_qty(self):
        """
        Получение количества тайлов по длине и ширине
        """
        elem_qty_x = self.map_pixmap.width() // MapsData.STATIC_TILE_SIZE
        elem_qty_y = self.map_pixmap.height() // MapsData.STATIC_TILE_SIZE
        return elem_qty_x, elem_qty_y

    def calculate_grid_step(self):
        """
        Получение шага координатной сетки
        """
        grid_step_x = self.map_pixmap.width() // self.elem_qty_x  # Шаг по оси X
        grid_step_y = self.map_pixmap.height() // self.elem_qty_y  # Шаг по оси Y
        return grid_step_x, grid_step_y

    def update_map(self, map_path):
        """
        Обновление карты с очисткой сетки
        """
        self.scene.clear()

        self.map_pixmap = QPixmap(map_path)
        self.map_item = QGraphicsPixmapItem(self.map_pixmap)
        self.scene.addItem(self.map_item)

        self.elem_qty_x, self.elem_qty_y = self.calculate_elem_qty()
        self.grid_step_x, self.grid_step_y = self.calculate_grid_step()

        self.draw_grid()


class NoScrollComboBox(QComboBox):
    """
    Виджет комбобокс, без скролла
    """

    def wheelEvent(self, event):
        event.ignore()


class HMApp(QMainWindow):
    """
    Основное окно
    Орбитальная система наведения HellMachine
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle('HellMachine')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        self.coord_label = QLabel('Координаты на сетке: X=0, Y=0', parent=self)
        self.main_layout.addWidget(self.coord_label)

        self.map_widget = MapWidget(self.coord_label, MapsData.get_map_url('lv624'))
        self.main_layout.addWidget(self.map_widget)

        self.map_layout = QVBoxLayout()
        self.map_selector_label = QLabel('Выбранная карта', self)
        self.map_selector_widget = NoScrollComboBox(self)
        self.map_selector_widget.currentIndexChanged.connect(self.on_map_select)

        self.map_lz_selector_label = QLabel('Зона посадки', self)
        self.map_lz_selector_widget = NoScrollComboBox(self)

        self.map_layout.addWidget(self.map_selector_label)
        self.map_layout.addWidget(self.map_selector_widget)
        self.main_layout.addWidget(self.map_lz_selector_label)
        self.main_layout.addWidget(self.map_lz_selector_widget)

        self.map_container = QWidget(self)
        self.map_container.setLayout(self.map_layout)
        self.main_layout.addWidget(self.map_container)

        self.get_maps()

    def on_map_select(self):
        """
        Обработчик переключения карты
        """
        map_name = self.map_selector_widget.currentText()
        map_path = MapsData.get_map_url(map_name)
        self.map_widget.update_map(map_path)
        self.get_lz_zones()

    def get_lz_zones(self):
        """
        Получение зон посадки на карте
        """
        self.map_lz_selector_widget.clear()
        map_name = self.map_selector_widget.currentText().lower()
        self.map_lz_selector_widget.addItems(MapsData.get_zones_for_map(map_name))

    def get_maps(self):
        """
        Получение всех карт
        """
        maps_dir = config.get_map_dir()
        try:
            files = os.listdir(maps_dir)
            # Откидываем расширение из имени
            files_names = [file_name[:-4].upper() for file_name in files if file_name.endswith('.png')]
            self.map_selector_widget.addItems(files_names)
        except FileNotFoundError:
            print(f'Папка {maps_dir} не найдена')
