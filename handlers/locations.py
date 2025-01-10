from aiogram import Router, F, types
from aiogram.types import InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from handlers.text_commands import commands
from models.db import Session
import handlers.utils as utils
from weather_requests.weather import weather

router = Router()

@router.callback_query(F.data == commands.my_locations)
async def get_my_locations(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_locations = None
    async with Session() as session:
        user_locations = await utils.get_user_locations(user_id, session)

    builder = InlineKeyboardBuilder()
    for location in user_locations:
        builder.row(InlineKeyboardButton(
            text=location.name,
            callback_data=commands.get_location_weather(location.name)
            ))
    builder.row(InlineKeyboardButton(text=commands.add_location, callback_data=commands.add_location))
    builder.row(InlineKeyboardButton(text='Обратно в меню', callback_data=commands.get_menu))

    await callback.message.answer("Ваши локации", reply_markup=builder.as_markup())
    await types.Message.delete(callback.message)

@router.callback_query(F.data.contains(commands.get_location_weather("")))
async def get_weather_in_location(callback: CallbackQuery):
    command = commands.get_location_weather("")
    user_id = callback.from_user.id
    data = callback.data
    location_name = data[data.find(command) + len(command):]
    location = None
    async with Session() as session:
        location = await utils.check_location_exists(user_id, location_name, session)

    forecast = None
    try:
        forecast = await weather.get_weather_forecast(
            location.latitude,
            location.longitude,
            number_of_days=2,
            weather_now=True
        )
    except Exception as err:
        print(err)
        forecast = "Извините произошла ошибка при обращении к open-meteo. Попробуйте позднее"
    
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Удалить локацию', callback_data=commands.delete_location(location.id)))
    builder.row(InlineKeyboardButton(text='Обратно в меню', callback_data=commands.get_menu))
    await callback.message.answer(text=forecast, reply_markup=builder.as_markup())
    await types.Message.delete(callback.message)

@router.callback_query(
    F.data.contains(commands.delete_location(''))
)
async def delete_location(callback: types.CallbackQuery):
    command = commands.delete_location('')
    data = callback.data
    location_id = data[data.find(command) + len(command):]
    async with Session() as session:
        try:
            await utils.delete_location(int(location_id), session)
        except LookupError:
            await callback.mesage.answer('хмм... Похоже эта локация уже была удалена')
    await callback.message.answer('Локация успешно удалена')


class CreateLocation(StatesGroup):
    choosing_name = State()
    getting_location = State()


@router.callback_query(StateFilter(None), F.data == commands.add_location)
async def add_location(callback: CallbackQuery, state: FSMContext):
    kb = [[KeyboardButton(text='Дом'), KeyboardButton(text='Дача'), KeyboardButton(text='Работа')]]
    await callback.message.answer(
        "Выберите или придумайте сами имя для новой локации",
        reply_markup=ReplyKeyboardMarkup(keyboard=kb, one_time_keyboard=True)
        )
    await state.set_state(CreateLocation.choosing_name)

@router.message(StateFilter(CreateLocation.choosing_name))
async def choose_location_name(message: types.Message, state: FSMContext):
    name = message.text
    user_id = message.from_user.id
    location_exists = False
    async with Session() as session:
        if await utils.check_location_exists(user_id, name, session):
            location_exists = True

    error_comment = None
    if len(name) == 0:
        error_comment = 'Имя не может быть пустым'
    if len(name) > 25:
        error_comment = 'Имя слишком длинное'
    if location_exists:
        error_comment = 'У вас уже есть локация с данным именем'
    
    if error_comment:
        kb = [[KeyboardButton(text='Дом'), KeyboardButton(text='Дача'), KeyboardButton(text='Работа')]]
        await message.answer(
            error_comment,
            reply_markup=ReplyKeyboardMarkup(keyboard=kb, one_time_keyboard=True)
        )
        return
    await state.update_data(location_name=message.text)
    await state.set_state(CreateLocation.getting_location)
    await message.answer(
        text='Выберите нужную локацию и отправьте ее боту'
    )

@router.message(StateFilter(CreateLocation.getting_location), F.location)
async def choose_location_geo(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    location_name = data['location_name']
    user_id = message.from_user.id
    obj_data = {
        "name": location_name,
        "latitude": message.location.latitude,
        "longitude": message.location.longitude,
        "user_id": user_id,
    } 
    async with Session() as session:
        location = await utils.create_location(obj_data, session)
    await message.answer('Локация добавлена успешно')
    await state.set_state(None)
