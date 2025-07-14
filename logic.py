from utils import is_within_city
from services import get_distance_km

def calculate_out_of_city_price(
    start: tuple, end: tuple, transport_rate: float
) -> float:
    """Розрахунок для перевезень за межами Львова."""
    from config import LVIV_CENTER

    if is_within_city(*start):
        border_to_start = 0
    else:
        border_to_start = get_distance_km(LVIV_CENTER, start) - 10

    route_distance = get_distance_km(start, end)

    total_distance = border_to_start + route_distance
    price = 900 + total_distance * 2 * transport_rate
    return round(price, 2)