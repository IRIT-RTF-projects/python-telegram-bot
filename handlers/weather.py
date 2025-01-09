from aiogram import Router, F, types
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from handlers.text_commands import commands
from weather_requests.weather import weather

router = Router()


@router.message(F.location)
async def send_weather_in_location(message: Message):
    latitude, longitude = message.location.latitude, message.location.longitude
    forecast = await weather.get_weather_forecast(latitude, longitude, number_of_days=1, weather_now=True)
    await message.answer(text=forecast)
    await Message.delete(message)

@router.callback_query(F.data == commands.request_location)
async def request_location(callback: types.CallbackQuery):
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text='Отправить текущую геопозицию', request_location=True))
    await callback.message.answer("Отправьте геопозицию", reply_markup=builder.as_markup(one_time_keyboard=True, resize_keyboard=True))
