from aiogram import F, Router, types
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.text_commands import commands
from presets import get_help_text

router = Router()


@router.callback_query(F.data == commands.get_help)
async def get_my_locations(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text='Обратно в меню', callback_data=commands.get_menu)
    )
    await callback.message.answer(
        get_help_text(), reply_markup=builder.as_markup()
    )
    await types.Message.delete(callback.message)
