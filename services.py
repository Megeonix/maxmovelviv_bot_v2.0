import requests
from config import ORS_API_KEY

def get_distance_km(start, end) -> float:
    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
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

# Функція для відправки заявки всім адміністраторам
async def send_admins_order(bot, order_text, admin_ids):
    for admin_id in admin_ids:
        try:
            await bot.send_message(admin_id, order_text)
        except Exception as e:
            print(f"Не вдалося надіслати повідомлення адміну {admin_id}: {e}")

# Якщо потрібно: заглушка (наприклад, отримати адресу за координатами)
def geocode_coords(coords):
    # Можна підключити ORS reverse geocoding або залишити заглушку
    return f"https://maps.google.com/?q={coords[0]},{coords[1]}"
