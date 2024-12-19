from base.settings import config


class MapsData:
    """
    Статичные данные карты
    """

    STATIC_TILE_SIZE = 32  # Размер тайла на всех картах примерно 32 на 32px
    ZONES_COORDINATES = {
        'lv624': {
            'east': {'coords': (147, 36), 'direction': 'Восток', 'label': 'Середина взлетки у фонаря ЗП-1'},
            'west': {'coords': (44, 45), 'direction': 'Запад', 'label': 'Терминал вызова шаттла ЗП-2'},
        },
        'lv522': {
            'east': {'coords': (165, 33), 'direction': 'Восток', 'label': 'Выше носа шаттла, правый фонарь ЗП-1'},
            'west': {'coords': (23, 53), 'direction': 'Запад', 'label': 'Правый угол взлетки ЗП-2'},
        },
        'solaris': {
            'north': {'coords': (33, 204), 'direction': 'Север', 'label': 'Правый угол взлетки ЗП-1'},
            'south': {'coords': (39, 104), 'direction': 'Юг', 'label': 'Правый угол взлетки ЗП-2'},
        },
        'kutjevo': {
            'north': {'coords': (30, 144), 'direction': 'Север', 'label': 'Правый угол взлетки Посадочная зона'},
            'south': {'coords': (23, 47), 'direction': 'Юг', 'label': 'Правый угол взлетки Дюны'},
        },
        'fiorina': {
            'north': {'coords': (242, 125), 'direction': 'Север', 'label': 'Правый угол взлетки ЗП-1'},
            'south': {'coords': (167, 42), 'direction': 'Юг', 'label': 'Правый угол взлетки ЗП-2'},
        },
        'shivas': {
            'north': {'coords': (30, 150), 'direction': 'Север', 'label': 'Правый угол взлетки ЗП-2'},
            'south': {'coords': (30, 42), 'direction': 'Юг', 'label': 'Справа дерево у взлетки ЗП-1'},
        },
        'trijent': {
            'north': {'coords': (40, 215), 'direction': 'Север', 'label': 'Правый угол взлетки ЗП-1'},
            'south': {'coords': (27, 35), 'direction': 'Юг', 'label': 'Правый угол взлетки ЗП-2'},
        },
        'varadero': {
            'west': {'coords': (76, 153), 'direction': 'Запад', 'label': 'Правый угол взлетки ЗП-1'},
            'east': {'coords': (148, 159), 'direction': 'Восток', 'label': 'Справа от носа шаттла ЗП-2'},
        },
    }

    @classmethod
    def get_zones_for_map(cls, map_name):
        """
        Возвращает доступные зоны посадки на карте
        """
        res = cls.ZONES_COORDINATES.get(map_name, {}).keys()
        return cls.ZONES_COORDINATES.get(map_name, {}).keys()

    @classmethod
    def get_zone_info(cls, map_name, zone):
        """
        Возвращает информацию о зоне посадки
        """
        return cls.ZONES_COORDINATES.get(map_name, {}).get(zone)

    @staticmethod
    def get_map_url(name) -> str:
        """
        Возвращает путь до изображения карты
        """
        return f'{config.get_map_dir()}/{name.lower()}.png'
