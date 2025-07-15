from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode

from keyboards import (
    start_kb,
    service_kb,
    transport_kb,
    hours_kb,
    confirm_kb,
    cargo_type_kb,
)

from logic import (
    calculate_city_price,
    calculate_out_of_city_price,
)

from utils import MIN_HOURS, CITY_PRICES, OUT_CITY_PRICES
from services import get_distance_km
from units import FSMOrder
from texts import (
    START_TEXT,
    LOCATION_HINT,
    CONFIRM_TEXT,
    SERVICE_CONFIRM_TEMPLATE,
    SERVICE_UTIL_TEMPLATE,
    SERVICE_MOVE_TEMPLATE,
    SEND_PHONE,
)

