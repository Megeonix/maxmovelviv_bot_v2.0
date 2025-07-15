from utils import is_within_city
from services import get_distance_km

def calculate_city_price(car_type: str, hours: float, city_prices: dict, min_hours: dict) -> float:
    """
    Рахує ціну перевезення по місту Львів:
    - враховує мінімальні години для кожного авто
    - тариф за годину для відповідного авто
    """
    hours = max(hours, min_hours.get(car_type, 2))
    price_per_hour = city_prices.get(car_type)
    if price_per_hour is None:
        return 0.0  # для "по домовленості"
    return round(hours * price_per_hour, 2)

def calculate_out_city_price(start: tuple, end: tuple, car_type: str, out_city_prices: dict) -> float:
    """
    Рахує ціну перевезення за межі Львова:
    900 грн. + (відстань від межі Львова до точки завантаження + відстань між точками)
    * 2 * тариф для типу авто (грн/км)
    """
    from config import LVIV_CENTER, CITY_RADIUS_KM

    km_from_center_to_start = get_distance_km(LVIV_CENTER, start)
    # Якщо точка завантаження всередині міста — цю частину не додаємо
    extra_km = max(km_from_center_to_start - CITY_RADIUS_KM, 0)
    route_distance = get_distance_km(start, end)
    km_price = out_city_prices.get(car_type)
    if km_price is None:
        return 0.0  # для "по домовленості"
    full_km = extra_km + route_distance
    price = 900 + full_km * 2 * km_price
    return round(price, 2)

def calculate_cargo_work_price(work_type: str, hours: float) -> float:
    """
    Вартість вантажних робіт по місту.
    """
    # Квартирний або офісний переїзд — 300 грн/год (мінімум 2 години)
    if work_type == "Квартирний або офісний переїзд":
        return round(max(hours, 2) * 300, 2)
    # Будівельні матеріали — 400 грн + 7 грн поверх або 21 грн ліфт (рахується в handler'і)
    if work_type == "Будівельні матеріали":
        return 400  # Мінімалка, далі уточнює менеджер
    # Такелажні роботи — по домовленості
    if work_type == "Такелажні роботи":
        return 0.0
    return 0.0

def minimum_hours_for_car(car_type: str, min_hours: dict) -> int:
    """
    Повертає мінімальну кількість годин для конкретного авто
    """
    return min_hours.get(car_type, 2)

def is_by_agreement(car_type: str) -> bool:
    """
    Для авто 'по домовленості' (наприклад, 10т або інше авто) повертає True
    """
    return car_type in ("Фургон до 10т до 70м3", "Інше авто")
