import requests
from config import ORS_API_KEY

def get_distance_km(start, end) -> float:
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {"Authorization": ORS_API_KEY, "Content-Type": "application/json"}
    body = {
        "coordinates": [
            [start[1], start[0]],
            [end[1], end[0]]
        ]
    }
    try:
        response = requests.post(url, json=body, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        dist_m = data['features'][0]['properties']['segments'][0]['distance']
        return dist_m / 1000
    except Exception as e:
        print("Error getting distance:", e)
        return 0
