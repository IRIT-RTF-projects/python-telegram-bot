from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import handlers.utils as utils
from handlers.text_commands import commands
from models.db import Session

router = Router()


def get_main_menu_markup() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = [
        [
            InlineKeyboardButton(
                text=commands.my_locations,
                callback_data=commands.my_locations
            )
        ],
        [
            InlineKeyboardButton(
                text=commands.my_subscriptions,
                callback_data=commands.my_subscriptions
            )
        ],
        [
            InlineKeyboardButton(
                text=commands.weather_now,
                callback_data=commands.request_location
            )
        ],
        [
            InlineKeyboardButton(
                text=commands.get_help,
                callback_data=commands.get_help
            )
        ],
    ]
    for row in buttons:
        builder.row(*row)
    return builder.as_markup()


@router.message(Command("start"))
async def get_main_menu(message: types.Message) -> None:
    async with Session() as session:
        user_id = message.from_user.id
        chat_id = message.chat.id
        db_user = await utils.get_user_by_id(user_id, session)
        if not db_user:
            db_user = await utils.register_user(user_id, chat_id, session)
            await message.answer("Поздравляем ваш юзер успешно зарегистрирован")
        await message.answer(
            'Главное меню',
            reply_markup=get_main_menu_markup()
        )


@router.callback_query(F.data == commands.get_menu)
async def get_main_menu_via_callback(callback: types.CallbackQuery) -> None:
    await callback.message.answer(
        'Главное меню',
        reply_markup=get_main_menu_markup()
    )
    await callback.answer()
    await types.Message.delete(callback.message)
