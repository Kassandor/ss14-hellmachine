import sys

from PyQt5.QtWidgets import QApplication

from src.controllers.map_controllers import MapGraphicsViewController
from src.models.map import MapsData
from src.views.main_window import HMApp


def main():
    app = QApplication(sys.argv)
    main_window = HMApp()
    maps_data = MapsData()
    map_graphics_controller = MapGraphicsViewController(main_window.map_widget.map_graphics, maps_data)
    map_graphics_controller.load_map('lv624')
    main_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
