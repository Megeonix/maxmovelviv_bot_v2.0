from geopy.distance import geodesic
from config import BASE_OUTSIDE_CITY_COST

# Ціни за км для кожного типу авто (за містом)
KM_RATES = {
    "Бус до 1,5 т до 13м3": 20,
    "Бус максі база до 2 т до 15 м3": 20,
    "Фургон до 2 т до 20 м3": 25,
    "Фургон до 2 т до 20 м3 з гідробортом": 25,
    "Фургон до 3 т гідроборт до 30м3": 27,
    "Фургон 5т гідроборт до 40м3": 27,
    "Фургон до 10т до 70м3": None,  # по домовленості
    "Інше авто": None  # по домовленості
}

# Ціни по місту (за годину) + мінімальні години
CITY_RATES = {
    "Бус до 1,5 т до 13м3": (450, 2),
    "Бус максі база до 2 т до 15 м3": (450, 2),
    "Фургон до 2 т до 20 м3": (650, 2),
    "Фургон до 2 т до 20 м3 з гідробортом": (700, 3),
    "Фургон до 3 т гідроборт до 30м3": (640, 3),
    "Фургон 5т гідроборт до 40м3": (850, 3),
    "Фургон до 10т до 70м3": (None, 3),  # по домовленості
    "Інше авто": (None, 3),  # по домовленості
}

# Ціни на вантажні роботи
LOADING_RATES = {
    "Квартирний або офісний переїзд": (300, 2),  # грн/год, мін. 2 год
    "Будівельні матеріали": (400, 0),  # 400 + поверх/ліфт логіка окремо
    "Такелажні роботи": (None, 0)  # по домовленості
}


def calculate_city_price(vehicle: str, hours: int) -> int | str:
    rate, min_hours = CITY_RATES.get(vehicle, (None, None))
    if rate is None:
        return "Ціна по домовленості"
    total_hours = max(hours, min_hours)
    return rate * total_hours


def calculate_loading_price(type_: str, floors: int = 0, by_elevator: bool = False, units: int = 1, hours: int = 2) -> int | str:
    if type_ == "Квартирний або офісний переїзд":
        rate, min_hours = LOADING_RATES[type_]
        return rate * max(hours, min_hours)
    elif type_ == "Будівельні матеріали":
        base_price = 400
        if by_elevator:
            lift_price = units * 21
        else:
            lift_price = units * floors * 7
        return base_price + lift_price
    elif type_ == "Такелажні роботи":
        return "Ціна по домовленості"
    return 0


def calculate_outside_city_price(vehicle: str, load_coords: tuple, unload_coords: tuple, lviv_border_coords: tuple) -> int | str:
    km_rate = KM_RATES.get(vehicle)
    if km_rate is None:
        return "Ціна по домовленості"
    
    distance_from_lviv_to_load = geodesic(lviv_border_coords, load_coords).km
    distance_between = geodesic(load_coords, unload_coords).km
    total_km = (distance_from_lviv_to_load + distance_between) * 2
    return int(BASE_OUTSIDE_CITY_COST + total_km * km_rate)
