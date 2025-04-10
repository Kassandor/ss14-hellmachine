from PyQt5.QtWidgets import QComboBox


class NoScrollComboBox(QComboBox):
    """
    Виджет комбобокс, без скролла
    """

    @staticmethod
    def wheelEvent(event) -> None:
        event.ignore()
