from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, Location
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import main_menu_kb, service_kb, transport_kb, hours_kb, confirm_kb, cargo_type_kb
from texts import *
from logic import (
    is_within_city,
    calculate_city_price,
    calculate_out_city_price,
    calculate_cargo_work_price,
)
from services import send_admins_order, geocode_coords

router = Router()


class OrderFSM(StatesGroup):
    transport_type = State()
    from_location = State()
    to_location = State()
    cargo_work_type = State()
    hours = State()
    description = State()
    phone = State()
    confirm = State()


@router.message(F.text.lower() == "start" or F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_kb)


@router.message(F.text == "По місту Львів")
async def choose_service_city(message: Message, state: FSMContext):
    await state.update_data(transfer_type="city")
    await message.answer(CHOOSE_SERVICE_TEXT, reply_markup=service_kb)


@router.message(F.text == "За містом Львів")
async def choose_service_intercity(message: Message, state: FSMContext):
    await state.update_data(transfer_type="intercity")
    await message.answer(CHOOSE_SERVICE_TEXT, reply_markup=service_kb)


@router.message(F.text.in_(["Перевезення вантажу", "Вантажні роботи + перевезення вантажу"]))
async def choose_transport(message: Message, state: FSMContext):
    await state.update_data(service=message.text)
    await message.answer(CHOOSE_TRANSPORT_TEXT, reply_markup=transport_kb)
    await state.set_state(OrderFSM.transport_type)


@router.message(OrderFSM.transport_type)
async def get_from_location(message: Message, state: FSMContext):
    await state.update_data(transport_type=message.text)
    await message.answer(SEND_FROM_LOCATION_TEXT)
    await message.answer(GEOLOCATION_TIP)
    await state.set_state(OrderFSM.from_location)


@router.message(OrderFSM.from_location, F.location)
async def get_to_location(message: Message, state: FSMContext):
    await state.update_data(from_location=(message.location.latitude, message.location.longitude))
    await message.answer(SEND_TO_LOCATION_TEXT)
    await message.answer(GEOLOCATION_TIP)
    await state.set_state(OrderFSM.to_location)


@router.message(OrderFSM.to_location, F.location)
async def process_locations(message: Message, state: FSMContext):
    await state.update_data(to_location=(message.location.latitude, message.location.longitude))
    data = await state.get_data()

    if data["service"] == "Вантажні роботи + перевезення вантажу":
        await message.answer(CHOOSE_CARGO_WORK_TYPE_TEXT, reply_markup=cargo_type_kb)
        await state.set_state(OrderFSM.cargo_work_type)
    else:
        if data["transfer_type"] == "city":
            await message.answer(CHOOSE_HOURS_TEXT, reply_markup=hours_kb)
            await state.set_state(OrderFSM.hours)
        else:
            # Intercity transfer
            price, distance_km = await calculate_intercity_price(data)
            await state.update_data(price=price, distance=distance_km)
            await message.answer(
                f"Орієнтовна відстань: {distance_km} км\n"
                f"Орієнтовна вартість: {price} грн",
                reply_markup=confirm_kb,
            )
            await state.set_state(OrderFSM.confirm)


@router.message(OrderFSM.cargo_work_type)
async def choose_hours_for_combo(message: Message, state: FSMContext):
    await state.update_data(cargo_work_type=message.text)
    await message.answer(CHOOSE_HOURS_TEXT, reply_markup=hours_kb)
    await state.set_state(OrderFSM.hours)


@router.message(OrderFSM.hours)
async def final_price_city(message: Message, state: FSMContext):
    try:
        hours = int(message.text)
        await state.update_data(hours=hours)
    except ValueError:
        await message.answer("Введіть число годин.")
        return

    data = await state.get_data()

    if data["service"] == "Вантажні роботи":
        price = calculate_cargo_work_price(data)
    else:
        price = calculate_city_price(data)

    await state.update_data(price=price)
    await message.answer(f"Орієнтовна вартість: {price} грн", reply_markup=confirm_kb)
    await state.set_state(OrderFSM.confirm)


@router.message(F.text == "Вантажні роботи")
async def standalone_cargo_work(message: Message, state: FSMContext):
    await state.update_data(service=message.text)
    await message.answer(SEND_WORK_LOCATION_TEXT)
    await message.answer(GEOLOCATION_TIP)
    await state.set_state(OrderFSM.from_location)


@router.message(OrderFSM.from_location, F.location)
async def get_cargo_work_location(message: Message, state: FSMContext):
    await state.update_data(from_location=(message.location.latitude, message.location.longitude))
    await message.answer(CHOOSE_CARGO_WORK_TYPE_TEXT, reply_markup=cargo_type_kb)
    await state.set_state(OrderFSM.cargo_work_type)


@router.message(F.text == "Такелажні роботи")
async def special_work_description(message: Message, state: FSMContext):
    await state.update_data(service="Такелажні роботи")
    await message.answer(SPECIAL_WORK_PROMPT)
    await state.set_state(OrderFSM.description)


@router.message(F.text == "Утилізація сміття")
async def garbage_removal(message: Message, state: FSMContext):
    await state.update_data(service="Утилізація сміття")
    await message.answer(GARBAGE_PROMPT)
    await state.set_state(OrderFSM.description)


@router.message(OrderFSM.description)
async def ask_phone(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Вкажіть ваш номер телефону:")
    await state.set_state(OrderFSM.phone)


@router.message(OrderFSM.confirm, F.text == "Підтвердити")
async def ask_phone_final(message: Message, state: FSMContext):
    await message.answer("Вкажіть ваш номер телефону:")
    await state.set_state(OrderFSM.phone)


@router.message(OrderFSM.confirm, F.text == "Скасувати")
async def cancel_order(message: Message, state: FSMContext):
    await message.answer("Заявку скасовано. Ви можете почати заново: /start")
    await state.clear()


@router.message(OrderFSM.phone)
async def finish_order(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()

    location_name = await geocode_coords(data.get("from_location"))
    msg = await send_admins_order(message.from_user.full_name, data, location_name)
    await message.answer("Заявку надіслано. Наш менеджер зв’яжеться з вами.")
    await state.clear()
