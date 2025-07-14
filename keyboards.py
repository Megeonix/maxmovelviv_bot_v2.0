# keyboards.py

from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_transport_type_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="По місту", callback_data="transport_city")
    builder.button(text="За містом", callback_data="transport_outside")
    builder.adjust(2)
    return builder.as_markup()

def get_services_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="1️⃣ Перевезення вантажу", callback_data="service_transport")
    builder.button(text="2️⃣ Вантажні роботи + перевезення", callback_data="service_combo")
    builder.button(text="3️⃣ Вантажні роботи", callback_data="service_loading_only")
    builder.button(text="4️⃣ Утилізація сміття", callback_data="service_utilization")
    builder.adjust(1)
    return builder.as_markup()

def get_vehicle_kb():
    builder = InlineKeyboardBuilder()
    vehicles = [
        ("1. Бус до 1.5т до 13м3", "vehicle_1"),
        ("2. Бус максі база до 2т до 15м3", "vehicle_2"),
        ("3. Фургон до 2т до 20м3", "vehicle_3"),
        ("4. Фургон до 2т до 20м3 з гідробортом", "vehicle_4"),
        ("5. Фургон до 3т гідроборт до 30м3", "vehicle_5"),
        ("6. Фургон 5т гідроборт до 40м3", "vehicle_6"),
        ("7. Фургон до 10т до 70м3", "vehicle_7"),
        ("8. Інше авто", "vehicle_8"),
    ]
    for name, callback in vehicles:
        builder.button(text=name, callback_data=callback)
    builder.adjust(1)
    return builder.as_markup()

def get_lifting_type_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="1️⃣ Квартирний/офісний переїзд", callback_data="lifting_move")
    builder.button(text="2️⃣ Будівельні матеріали", callback_data="lifting_build")
    builder.button(text="3️⃣ Такелажні роботи", callback_data="lifting_heavy")
    builder.adjust(1)
    return builder.as_markup()

def confirm_or_cancel_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Підтвердити", callback_data="confirm")
    builder.button(text="❌ Скасувати", callback_data="cancel")
    builder.adjust(2)
    return builder.as_markup()

def send_phone_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Надіслати номер телефону", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def remove_kb():
    return ReplyKeyboardRemove()
