# handlers.py

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, Location
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from states import OrderState
from keyboards import (
    get_transport_type_kb,
    get_services_kb,
    get_vehicle_kb,
    get_lifting_type_kb,
    confirm_or_cancel_kb,
    send_phone_kb,
    remove_kb,
)
from texts import START_TEXT, LOCATION_HINT
from services import get_vehicle_price, calculate_city_price, calculate_outside_price, get_lifting_price, get_distance
from utils import is_admin, send_order_to_admins

router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(START_TEXT)
    await message.answer("Оберіть тип перевезення:", reply_markup=get_transport_type_kb())


@router.callback_query(F.data.startswith("transport_"))
async def transport_type_selected(callback: CallbackQuery, state: FSMContext):
    transport_type = callback.data.split("_")[1]
    await state.update_data(transport_type=transport_type)
    await callback.message.answer("Оберіть послугу:", reply_markup=get_services_kb())


@router.callback_query(F.data.startswith("service_"))
async def service_selected(callback: CallbackQuery, state: FSMContext):
    service = callback.data.split("_")[1]
    await state.update_data(service=service)

    if service in ["transport", "combo"]:
        await callback.message.answer("Оберіть тип авто:", reply_markup=get_vehicle_kb())
    elif service == "loading":
        await callback.message.answer(LOCATION_HINT, reply_markup=remove_kb())
        await callback.message.answer("Надішліть локацію проведення вантажних робіт:")
        await state.set_state(OrderState.loading_location)
    elif service == "utilization":
        await callback.message.answer("Мінімальна вартість 1500 грн.\nВкажіть, що потрібно утилізувати:")
        await state.set_state(OrderState.utilization_description)


@router.callback_query(F.data.startswith("vehicle_"))
async def vehicle_selected(callback: CallbackQuery, state: FSMContext):
    vehicle_id = callback.data.split("_")[1]
    await state.update_data(vehicle_id=vehicle_id)
    await callback.message.answer(LOCATION_HINT, reply_markup=remove_kb())
    await callback.message.answer("Надішліть локацію завантаження:")
    await state.set_state(OrderState.pickup_location)


@router.message(OrderState.pickup_location, F.location)
async def pickup_location_received(message: Message, state: FSMContext):
    await state.update_data(pickup_location=(message.location.latitude, message.location.longitude))
    await message.answer("Надішліть локацію вивантаження:")
    await state.set_state(OrderState.dropoff_location)


@router.message(OrderState.dropoff_location, F.location)
async def dropoff_location_received(message: Message, state: FSMContext):
    await state.update_data(dropoff_location=(message.location.latitude, message.location.longitude))
    data = await state.get_data()
    transport_type = data["transport_type"]
    vehicle_id = data["vehicle_id"]
    pickup = data["pickup_location"]
    dropoff = data["dropoff_location"]
    service = data["service"]

    if service == "combo":
        await message.answer("Оберіть тип вантажних робіт:", reply_markup=get_lifting_type_kb())
        await state.set_state(OrderState.lifting_type)
    else:
        if transport_type == "city":
            await message.answer("Скільки годин потрібно? (мінімум згідно авто)")
            await state.set_state(OrderState.hours)
        else:
            distance_km = await get_distance(pickup, dropoff)
            await state.update_data(distance=distance_km)
            price = calculate_outside_price(vehicle_id, distance_km)
            await state.update_data(price=price)
            await message.answer(f"Орієнтовна вартість: {price} грн.", reply_markup=confirm_or_cancel_kb())


@router.message(OrderState.hours, F.text)
async def hours_received(message: Message, state: FSMContext):
    hours = int(message.text)
    data = await state.get_data()
    vehicle_id = data["vehicle_id"]
    price = calculate_city_price(vehicle_id, hours)
    await state.update_data(hours=hours, price=price)
    await message.answer(f"Орієнтовна вартість: {price} грн.", reply_markup=confirm_or_cancel_kb())


@router.callback_query(F.data.startswith("lifting_"))
async def lifting_type_selected(callback: CallbackQuery, state: FSMContext):
    lifting_type = callback.data.split("_")[1]
    await state.update_data(lifting_type=lifting_type)
    if lifting_type == "move":
        await callback.message.answer("Скільки годин потрібно? (мінімум 2)")
        await state.set_state(OrderState.hours)
    elif lifting_type == "build":
        await callback.message.answer("Вкажіть кількість одиниць та поверх (або 'ліфт'):")
        await state.set_state(OrderState.building_input)
    else:
        await callback.message.answer("Опишіть, які саме такелажні роботи потрібні:")
        await state.set_state(OrderState.heavy_description)


@router.message(OrderState.utilization_description)
async def utilization_desc_received(message: Message, state: FSMContext):
    await state.update_data(utilization_desc=message.text)
    await message.answer("Вкажіть свій номер телефону:", reply_markup=send_phone_kb())
    await state.set_state(OrderState.phone)


@router.message(OrderState.heavy_description)
async def heavy_desc_received(message: Message, state: FSMContext):
    await state.update_data(heavy_desc=message.text)
    await message.answer("Вкажіть свій номер телефону:", reply_markup=send_phone_kb())
    await state.set_state(OrderState.phone)


@router.message(OrderState.phone, F.contact)
async def phone_received(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    data = await state.get_data()
    await send_order_to_admins(data)
    await message.answer("Дякуємо! Заявку надіслано.", reply_markup=remove_kb())
    await state.clear()
