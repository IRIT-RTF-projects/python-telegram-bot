from aiogram import Router, F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder 
from aiogram.types import InlineKeyboardButton

from handlers.text_commands import commands

router = Router()

@router.callback_query(F.data == commands.my_subscriptions)
async def get_my_locations(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Обратно в меню', callback_data=commands.get_menu))
    await callback.message.answer("ваши подписки на погоду", reply_markup=builder.as_markup())
    await types.Message.delete(callback.message)