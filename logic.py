from utils import is_within_city
from services import get_distance_km
from config import LVIV_CENTER

def calculate_out_of_city_price(
    start: tuple, end: tuple, transport_rate: float
) -> float:
    """Розрахунок для перевезень за межами Львова."""
    if is_within_city(*start):
        border_to_start = 0
    else:
        border_to_start = get_distance_km(LVIV_CENTER, start) - 10

    route_distance = get_distance_km(start, end)
    total_distance = border_to_start + route_distance
    price = 900 + total_distance * 2 * transport_rate
    return round(price, 2)

def calculate_city_price(car_type: str, hours: int, city_prices: dict, min_hours: dict) -> int:
    """Розрахунок вартості перевезення по місту"""
    hourly_rate = city_prices.get(car_type)
    min_time = min_hours.get(car_type, 1)
    effective_hours = max(hours, min_time)
    return hourly_rate * effective_hours
