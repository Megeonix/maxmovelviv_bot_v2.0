from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Головне меню
main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚚 По місту Львів")],
        [KeyboardButton(text="🌍 За містом Львів")]
    ],
    resize_keyboard=True
)

# Вибір послуги
service_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Перевезення вантажу")],
        [KeyboardButton(text="Вантажні роботи + перевезення вантажу")],
        [KeyboardButton(text="Вантажні роботи (вантажники)")],
        [KeyboardButton(text="Утилізація сміття")]
    ],
    resize_keyboard=True
)

# Вибір типу транспорту
transport_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="1. Бус до 1,5 т до 13м3")],
        [KeyboardButton(text="2. Бус максі база до 2 т до 15 м3")],
        [KeyboardButton(text="3. Фургон до 2 т до 20 м3")],
        [KeyboardButton(text="4. Фургон до 2 т до 20 м3 з гідробортом")],
        [KeyboardButton(text="5. Фургон до 3 т гідроборт до 30м3")],
        [KeyboardButton(text="6. Фургон 5т гідроборт до 40м3")],
        [KeyboardButton(text="7. Фургон до 10т до 70м3")],
        [KeyboardButton(text="8. Інше авто")]
    ],
    resize_keyboard=True
)

# Вибір кількості годин (по місту)
hours_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="2"), KeyboardButton(text="3")],
        [KeyboardButton(text="4"), KeyboardButton(text="5")],
        [KeyboardButton(text="6"), KeyboardButton(text="7")],
        [KeyboardButton(text="8"), KeyboardButton(text="9")],
        [KeyboardButton(text="10")]
    ],
    resize_keyboard=True
)

# Вибір типу вантажних робіт
cargo_type_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Квартирний або офісний переїзд")],
        [KeyboardButton(text="Будівельні матеріали")],
        [KeyboardButton(text="Такелажні роботи")]
    ],
    resize_keyboard=True
)

# Кнопки підтвердження чи скасування
confirm_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Підтвердити", callback_data="confirm")],
    [InlineKeyboardButton(text="❌ Скасувати", callback_data="cancel")]
])

# Кнопка надіслати геолокацію
location_button_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📍 Надіслати локацію", request_location=True)]
    ],
    resize_keyboard=True
)
