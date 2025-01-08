from aiogram import Router, F, types
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from handlers.text_commands import commands

router = Router()


@router.message(F.location)
async def send_weather_in_location(message: Message):
    await message.answer(str(message.location.latitude) + "  |  " + str(message.location.longitude))
    await Message.delete(message)

@router.callback_query(F.data == commands.request_location)
async def request_location(callback: types.CallbackQuery):
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text='Отправить локацию', request_location=True))
    await callback.message.answer("дайти погоду пжлста", reply_markup=builder.as_markup(one_time_keyboard=True, resize_keyboard=True))
