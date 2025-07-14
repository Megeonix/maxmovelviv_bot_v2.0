from geopy.distance import geodesic

# Центр Львова
CITY_CENTER = (49.8419, 24.0315)
CITY_RADIUS_KM = 10

def is_within_city(location: tuple[float, float]) -> bool:
    """
    Перевіряє, чи координати входять у радіус 10 км від центру Львова
    """
    return geodesic(location, CITY_CENTER).km <= CITY_RADIUS_KM
