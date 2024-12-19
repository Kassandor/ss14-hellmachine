import os


class Config:
    """
    Конфигурация проекта
    """

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MAP_DIR = BASE_DIR + '/static/maps'

    def get_base_dir(self):
        """
        Путь до базовой директории проекта
        """
        return self.BASE_DIR

    def get_map_dir(self):
        """
        Возвращает путь до папки с картами
        """
        return self.MAP_DIR


config = Config()
