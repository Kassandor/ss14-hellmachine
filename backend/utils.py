from datetime import timedelta, datetime


def get_next_fire_time() -> str:
    """
    Возвращение времени, когда возможен следующий выстрел
    """
    next_fire_time = datetime.now() + timedelta(minutes=10)
    return next_fire_time.strftime('%H:%M')
