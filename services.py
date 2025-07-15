import requests
from config import ORS_API_KEY, ADMIN_CHAT_IDS

# --- Отримати відстань через OpenRouteService ---
def get_distance_km(start, end) -> float:
    """
    Повертає відстань у км між двома точками через ORS directions API.
    start, end: (lat, lon)
    """
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

# --- Геокодування (отримати назву локації за координатами через ORS) ---
async def geocode_coords(coords):
    """
    Повертає рядок з адресою для координат (lat, lon)
    """
    try:
        url = f"https://api.openrouteservice.org/geocode/reverse"
        params = {
            "api_key": ORS_API_KEY,
            "point.lat": coords[0],
            "point.lon": coords[1],
            "size": 1
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data["features"]:
            return data["features"][0]["properties"].get("label", "Локація")
        else:
            return "Локація"
    except Exception as e:
        print("Error geocoding coords:", e)
        return "Локація"

# --- Надіслати заявку адміністраторам ---
from config import ADMIN_CHAT_IDS

async def send_admins_order(bot, data, location_name):
    """
    Відправка адміну заявки з усіма деталями.
    """
    # Формуємо текст заявки з data
    text = (
        f"📝 <b>Нова заявка</b>\n"
        f"Клієнт: {data.get('full_name') or '—'}\n"
        f"Телефон: {data.get('phone') or '—'}\n"
        f"Послуга: {data.get('service') or '—'}\n"
        f"Тип перевезення: {data.get('transfer_type') or '—'}\n"
        f"Тип транспорту: {data.get('transport_type') or '—'}\n"
        f"З локації: {location_name or data.get('from_location')}\n"
        f"В локацію: {data.get('to_location') or '—'}\n"
        f"Тип вантажних робіт: {data.get('cargo_work_type') or '—'}\n"
        f"Кількість годин: {data.get('hours') or '—'}\n"
        f"Опис: {data.get('description') or '—'}\n"
        f"Вартість: {data.get('price') or '—'} грн\n"
    )
    for admin_id in ADMIN_CHAT_IDS:
        try:
            await bot.send_message(admin_id, text)
        except Exception as e:
            print(f"Не вдалося надіслати адміну {admin_id}: {e}")
