import math
import os

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
    QLabel,
    QGraphicsEllipseItem,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)

from backend.maps_data import MapsData
from backend.utils import get_next_fire_time, Clipboard
from base.settings import config
from frontend.widgets import NoScrollComboBox


class MapWidget(QGraphicsView):
    """
    Виджет с картой
    """

    def __init__(self, label: QLabel, map_path: str) -> None:
        super().__init__()
        self.clipboard = Clipboard()
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
        self.grid_x = 0
        self.grid_y = 0

        # Атрибут для хранения текущей подсветки
        self.current_highlight = None

    def wheelEvent(self, event) -> None:
        """
        Реализация масштабирования при прокрутке колесика мыши
        """
        scale_factor = 1.5
        factor = scale_factor if event.angleDelta().y() > 0 else 1 / scale_factor
        self.scale(factor, factor)  # Масштабируем как по оси X, так и по оси Y

    def mousePressEvent(self, event) -> None:
        """
        Логика нажатия кнопки мыши
        """
        if event.button() == Qt.RightButton:
            click_pos = self.mapToScene(event.pos())

            # Переводим координаты Y так, чтобы Y рос вверх
            self.grid_x, self.grid_y = (
                math.ceil((click_pos.x() / self.grid_step_x) + self.dx),
                math.ceil(((self.map_pixmap.height() - click_pos.y()) / self.grid_step_y) + self.dy),
            )
            # Обновляем текст в QLabel
            self.label.setText(
                f"Координаты на сетке: X={self.grid_x}, Y={self.grid_y}, следующий выстрел в {get_next_fire_time()}"
            )
            self.clipboard.copy(f'{self.grid_x}, {self.grid_y}')

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
        self.draw_lines(self.prepare_grid_lines(), pen)

    def draw_lines(self, lines: list[tuple[int, int, int, int]], pen: QPen) -> None:
        """
        Отрисовка линий XY
        """
        for x1, y1, x2, y2 in lines:
            line_item = QGraphicsLineItem(x1, y1, x2, y2)
            line_item.setPen(pen)
            self.scene.addItem(line_item)

    def prepare_grid_lines(self) -> list[tuple[int, int, int, int]]:
        """
        Подготовка XY-линий
        """
        width = self.map_pixmap.width()
        height = self.map_pixmap.height()
        x_lines = [(x, 0, x, height) for x in range(0, width, self.grid_step_x)]
        y_lines = [(0, y, width, y) for y in range(0, height, self.grid_step_y)]
        return x_lines + y_lines

    def calculate_elem_qty(self) -> tuple[int, int]:
        """
        Получение количества тайлов по длине и ширине
        """
        elem_qty_x = self.map_pixmap.width() // MapsData.STATIC_TILE_SIZE
        elem_qty_y = self.map_pixmap.height() // MapsData.STATIC_TILE_SIZE
        return elem_qty_x, elem_qty_y

    def calculate_grid_step(self) -> tuple[int, int]:
        """
        Получение шага координатной сетки
        """
        grid_step_x = self.map_pixmap.width() // self.elem_qty_x  # Шаг по оси X
        grid_step_y = self.map_pixmap.height() // self.elem_qty_y  # Шаг по оси Y
        return grid_step_x, grid_step_y

    def clear_offset(self) -> None:
        """
        Очистка смещения, убирание подсветки квадрата
        """
        self.dx = 0
        self.dy = 0
        self.current_highlight = None

    def update_map(self, map_path: str) -> None:
        """
        Обновление карты с очисткой сетки
        """
        self.scene.clear()
        self.clear_offset()
        self.map_pixmap = QPixmap(map_path)
        self.map_item = QGraphicsPixmapItem(self.map_pixmap)
        self.scene.addItem(self.map_item)

        self.elem_qty_x, self.elem_qty_y = self.calculate_elem_qty()
        self.grid_step_x, self.grid_step_y = self.calculate_grid_step()

        self.draw_grid()


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

        self.map_layout.addWidget(self.map_selector_label)
        self.map_layout.addWidget(self.map_selector_widget)

        coord_input_layout = QHBoxLayout()
        self.game_x = QLineEdit(self)
        self.game_x.setPlaceholderText('X')
        self.game_y = QLineEdit(self)
        self.game_y.setPlaceholderText('Y')

        self.offset_button = QPushButton('Посчитать смещение', self)
        self.offset_button.clicked.connect(self.get_offset)

        coord_input_layout.addWidget(self.game_x)
        coord_input_layout.addWidget(self.game_y)
        coord_input_layout.addWidget(self.offset_button)
        self.main_layout.addLayout(coord_input_layout)

        # dx, dy
        self.dx_label = QLabel('Смещение Х: 0')
        self.dy_label = QLabel('Смещение Y: 0')
        self.main_layout.addWidget(self.dx_label)
        self.main_layout.addWidget(self.dy_label)

        self.map_container = QWidget(self)
        self.map_container.setLayout(self.map_layout)
        self.main_layout.addWidget(self.map_container)

        self.get_maps()
        self.on_map_select()

    def on_map_select(self) -> None:
        """
        Обработчик переключения карты
        """
        map_name = self.map_selector_widget.currentText()
        self.dx_label.clear()
        self.dy_label.clear()
        map_path = MapsData.get_map_url(map_name)
        self.map_widget.update_map(map_path)

    def get_maps(self) -> None:
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

    def get_offset(self) -> None:
        """
        Расчет смещения dx, dy
        """

        # todo: Допилить, вынести x,y в переменные класса map_widget
        print(self.map_widget.grid_x)
        print(self.map_widget.grid_y)
        self.map_widget.dx = int(self.game_x.text()) - self.map_widget.grid_x
        self.map_widget.dy = int(self.game_y.text()) - self.map_widget.grid_y
        self.dx_label.setText(f'Смещение X: {self.map_widget.dx}')
        self.dy_label.setText(f'Смещение Y: {self.map_widget.dy}')
