import requests
from config import ORS_API_KEY

def get_distance_km(start: tuple, end: tuple) -> float:
    """Отримує відстань у км між двома координатами через ORS."""
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {"Authorization": ORS_API_KEY}
    payload = {
        "coordinates": [[start[1], start[0]], [end[1], end[0]]],
        "units": "km"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    data = response.json()
    distance = data["features"][0]["properties"]["segments"][0]["distance"]  # в км
    return round(distance, 2)