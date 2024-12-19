from PyQt5.QtWidgets import QComboBox


class NoScrollComboBox(QComboBox):
    """
    Виджет комбобокс, без скролла
    """

    def wheelEvent(self, event):
        event.ignore()