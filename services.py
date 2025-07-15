import requests
from config import ORS_API_KEY, ADMIN_CHAT_IDS
from bot_instance import bot

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

async def send_admins_order(user_name, data, location_name=None):
    """Відправити заявку адміну(ам)"""
    text = f"<b>Нова заявка від {user_name}</b>\n\n"
    text += f"<b>Тип перевезення:</b> {data.get('transfer_type', '')}\n"
    text += f"<b>Послуга:</b> {data.get('service', '')}\n"
    text += f"<b>Тип транспорту:</b> {data.get('transport_type', '')}\n"
    if location_name:
        text += f"<b>Локація завантаження:</b> {location_name}\n"
    if data.get('from_location'):
        lat, lon = data['from_location']
        text += f"<b>Координати завантаження:</b> {lat}, {lon}\n"
    if data.get('to_location'):
        lat, lon = data['to_location']
        text += f"<b>Координати розвантаження:</b> {lat}, {lon}\n"
    if data.get('cargo_work_type'):
        text += f"<b>Тип вантажних робіт:</b> {data.get('cargo_work_type')}\n"
    if data.get('hours'):
        text += f"<b>Годин:</b> {data.get('hours')}\n"
    if data.get('description'):
        text += f"<b>Опис:</b> {data.get('description')}\n"
    if data.get('price'):
        text += f"<b>Ціна (розрахунок):</b> {data['price']} грн\n"
    if data.get('phone'):
        text += f"<b>Телефон:</b> {data['phone']}"

    # Надсилаємо всім адміністраторам
    for admin_id in ADMIN_CHAT_IDS:
        try:
            await bot.send_message(admin_id, text)
        except Exception as e:
            print(f"Не вдалося надіслати адміну {admin_id}: {e}")

async def geocode_coords(location: tuple) -> str:
    """Опціональна функція — повертає адресу по координатам (можеш дописати або замінити на заглушку)."""
    lat, lon = location
    return f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
