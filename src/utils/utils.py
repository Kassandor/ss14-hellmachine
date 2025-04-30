import platform
from datetime import timedelta, datetime

import pyperclip


class Clipboard:
    """
    Буфер обмена под windows, linux
    """

    def __init__(self):
        self.platform = platform.system()
        self.set_clipboard()

    def set_clipboard(self):
        platforms_clipboard = {'Linux': 'xclip', 'Windows': 'windows'}
        pyperclip.set_clipboard(platforms_clipboard.get(self.platform))

    @staticmethod
    def copy(text):
        pyperclip.copy(text)

    @staticmethod
    def paste():
        pyperclip.paste()


def get_next_fire_time() -> str:
    """
    Возвращение времени, когда возможен следующий выстрел
    """
    next_fire_time = datetime.now() + timedelta(minutes=10)
    return next_fire_time.strftime('%H:%M')
