from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

def start_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="По місту Львів"), KeyboardButton(text="За містом Львів")]
        ],
        resize_keyboard=True
    )

def service_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Перевезення вантажу")],
            [KeyboardButton(text="Вантажні роботи + перевезення вантажу")],
            [KeyboardButton(text="Вантажні роботи (вантажники)")],
            [KeyboardButton(text="Утилізація сміття")],
        ],
        resize_keyboard=True
    )

def location_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📍 Надіслати геолокацію", request_location=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def confirm_cancel_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="✅ Підтвердити"), KeyboardButton(text="❌ Скасувати")]],
        resize_keyboard=True
    )

def phone_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Надіслати номер телефону", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
