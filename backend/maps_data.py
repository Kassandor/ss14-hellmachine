from base.settings import config


class MapsData:
    """
    Статичные данные карты
    """

    STATIC_TILE_SIZE = 32  # Размер тайла на всех картах примерно 32 на 32px

    @staticmethod
    def get_map_url(name: str) -> str:
        """
        Возвращает путь до изображения карты
        """
        return f'{config.get_map_dir()}/{name.lower()}.png'
