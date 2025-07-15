from geopy.distance import geodesic
from config import LVIV_CENTER, CITY_RADIUS_KM

def is_within_city(location: tuple[float, float]) -> bool:
    """Чи координати входять у радіус 10 км від центру Львова"""
    return geodesic(location, LVIV_CENTER).km <= CITY_RADIUS_KM
