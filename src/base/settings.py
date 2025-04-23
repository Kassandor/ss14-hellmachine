from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """
    Конфигурация проекта
    """

    def get_map_dir(self) -> str:
        """
        Возвращает путь до папки с картами
        """
        return os.path.join(BASE_DIR, 'assets', 'maps')


config = Config()
