from utils import is_within_city
from services import get_distance_km
from config import LVIV_CENTER, CITY_RADIUS_KM

# Тарифи по місту (за годину)
CITY_PRICES = {
    "Бус до 1,5 т до 13м3": 450,
    "Бус максі база до 2 т до 15 м3": 450,
    "Фургон до 2 т до 20 м3": 650,
    "Фургон до 2 т до 20 м3 з гідробортом": 700,
    "Фургон до 3 т гідроборт до 30м3": 640,
    "Фургон 5т гідроборт до 40м3": 850
    # "Фургон до 10т до 70м3" і "Інше авто" – по домовленості
}

# Мінімальні години по авто
MIN_HOURS = {
    "Бус до 1,5 т до 13м3": 2,
    "Бус максі база до 2 т до 15 м3": 2,
    "Фургон до 2 т до 20 м3": 2,
    "Фургон до 2 т до 20 м3 з гідробортом": 3,
    "Фургон до 3 т гідроборт до 30м3": 3,
    "Фургон 5т гідроборт до 40м3": 3,
    "Фургон до 10т до 70м3": 3,
    "Інше авто": 3
}

# Тарифи за містом (за км)
OUT_CITY_PRICES = {
    "Бус до 1,5 т до 13м3": 20,
    "Бус максі база до 2 т до 15 м3": 20,
    "Фургон до 2 т до 20 м3": 25,
    "Фургон до 2 т до 20 м3 з гідробортом": 25,
    "Фургон до 3 т гідроборт до 30м3": 27,
    "Фургон 5т гідроборт до 40м3": 27
    # "Фургон до 10т до 70м3", "Інше авто" – по домовленості
}

# Вартість вантажних робіт
WORK_PRICES = {
    "Квартирний або офісний переїзд": 300,
    "Будівельні матеріали": 400,  # за одиницю
    "Такелажні роботи": 0  # по домовленості
}

def calculate_city_price(car_type: str, hours: int) -> str:
    if car_type not in CITY_PRICES:
        return "Вартість по домовленості (менеджер уточнить ціну)."
    min_hours = MIN_HOURS.get(car_type, 2)
    total_hours = max(hours, min_hours)
    price = CITY_PRICES[car_type] * total_hours
    price = round(price / 10) * 10
    return f"{price:.0f} грн (за {total_hours} год.)"

def calculate_out_of_city_price(start: tuple, end: tuple, car_type: str) -> str:
    if car_type not in OUT_CITY_PRICES:
        return "Вартість по домовленості (менеджер уточнить ціну)."
    tariff = OUT_CITY_PRICES[car_type]
    if is_within_city(start):
        border_to_start = 0
    else:
        border_to_start = max(0, get_distance_km(LVIV_CENTER, start) - CITY_RADIUS_KM)
    route_distance = get_distance_km(start, end)
    total_distance = border_to_start + route_distance
    price = 900 + total_distance * 2 * tariff
    price = round(price / 10) * 10
    return f"{price:.0f} грн (дистанція: {total_distance:.1f} км)"

def calculate_cargo_work_price(work_type: str, hours: int = 2, units: int = 1, floors: int = 0, by_lift: bool = False) -> str:
    if work_type == "Квартирний або офісний переїзд":
        price = WORK_PRICES[work_type] * max(hours, 2)
        return f"{price:.0f} грн (за {max(hours, 2)} год.)"
    elif work_type == "Будівельні матеріали":
        if by_lift:
            price = 400 + units * 21
            return f"{price:.0f} грн (вивантаження з ліфтом)"
        else:
            price = 400 + units * floors * 7
            return f"{price:.0f} грн (вивантаження по поверхах)"
    elif work_type == "Такелажні роботи":
        return "Вартість такелажних робіт визначається індивідуально, менеджер уточнить ціну."
    else:
        return "Вартість по домовленості."

def calculate_utilization_info():
    return "Мінімальна вартість утилізації сміття: 1500 грн. Для точної ціни вкажіть деталі й локацію — менеджер проконсультує."
