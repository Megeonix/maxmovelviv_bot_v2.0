import requests
from config import ORS_API_KEY, ADMIN_CHAT_IDS
from bot_instance import bot

def get_distance_km(start, end) -> float:
    """
    Отримує відстань (у км) між двома координатами через OpenRouteService.
    """
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

def geocode_coords(coords):
    """
    Формує короткий лінк на Google Maps по координатах.
    """
    if not coords:
        return "-"
    lat, lon = coords
    return f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

def make_admin_order_text(user_full_name: str, data: dict) -> str:
    """
    Формує текст заявки адміну з короткими посиланнями на Google Maps.
    """
    transfer_type = "По місту" if data.get("transfer_type") == "city" else "За містом"
    service = data.get("service", "")
    car_type = data.get("transport_type", "-")
    hours = data.get("hours", "-")
    price = data.get("price", "-")
    phone = data.get("phone", "-")
    from_coords = data.get("from_location")
    to_coords = data.get("to_location")
    description = data.get("description", "")

    msg = f"<b>Нова заявка!</b>\n"
    msg += f"👤 Клієнт: {user_full_name}\n"
    msg += f"Тип перевезення: {transfer_type}\n"
    msg += f"Послуга: {service}\n"
    if car_type and service and "вантажу" in service:
        msg += f"Тип транспорту: {car_type}\n"
    if from_coords:
        msg += (
            f"Локація завантаження: <a href='{geocode_coords(from_coords)}'>"
            f"{from_coords[0]:.6f}, {from_coords[1]:.6f}</a>\n"
        )
    if to_coords:
        msg += (
            f"Локація розвантаження: <a href='{geocode_coords(to_coords)}'>"
            f"{to_coords[0]:.6f}, {to_coords[1]:.6f}</a>\n"
        )
    if hours != "-":
        msg += f"Годин: {hours}\n"
    if price != "-":
        msg += f"Ціна: {price} грн\n"
    if phone:
        msg += f"Телефон: {phone}\n"
    if description:
        msg += f"Деталі/Опис: {description}\n"
    return msg

async def send_admins_order(user_full_name, data, location_name=None):
    """
    Надсилає заявку всім адміністраторам.
    """
    text = make_admin_order_text(user_full_name, data)
    for admin_id in ADMIN_CHAT_IDS:
        try:
            await bot.send_message(admin_id, text, parse_mode="HTML", disable_web_page_preview=True)
        except Exception as e:
            print(f"Не вдалося надіслати адміну {admin_id}: {e}")
