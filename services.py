from aiogram.types import Message
from aiogram.utils.formatting import Bold, Text
from geopy.point import Point
from geopy.distance import geodesic
from config import LVIV_CENTER

def get_hint_location() -> str:
    return (
        "📍 <b>Щоб надіслати локацію:</b>\n"
        "1. Натисніть скрепку 📎 або кнопку ➕ під полем введення\n"
        "2. Оберіть “Локація”\n"
        "3. Надішліть точку завантаження або вивантаження\n"
    )

def is_point_outside_lviv(user_point: Point, radius_km: float = 13.0) -> bool:
    """Перевірка, чи знаходиться точка за межами Львова (умовний радіус 13 км від центру)."""
    return geodesic((user_point.latitude, user_point.longitude), LVIV_CENTER).km > radius_km

def format_order_summary(data: dict) -> str:
    """Формує текст підсумку заявки для користувача чи адміністратора."""
    lines = [
        f"<b>Тип перевезення:</b> {data.get('delivery_type', '-')}",
        f"<b>Послуга:</b> {data.get('service_type', '-')}",
        f"<b>Тип авто:</b> {data.get('vehicle_type', '-')}",
        f"<b>Тип вантажних робіт:</b> {data.get('loading_type', '-')}",
        f"<b>Кількість годин:</b> {data.get('hours', '-')}",
        f"<b>Кількість одиниць:</b> {data.get('units', '-')}",
        f"<b>Поверхів (без ліфта):</b> {data.get('floors', '-')}",
        f"<b>Є ліфт:</b> {'Так' if data.get('by_elevator') else 'Ні'}",
        f"<b>Номер телефону:</b> {data.get('phone', '-')}",
        f"<b>Орієнтовна вартість:</b> <u>{data.get('price', 'не вказана')}</u>",
    ]

    if 'custom_note' in data:
        lines.append(f"<b>Опис:</b> {data['custom_note']}")

    return "\n".join([line for line in lines if line])
