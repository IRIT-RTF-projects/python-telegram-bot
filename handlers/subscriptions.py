from datetime import datetime

from aiogram import Router, F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder 
from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from models.db import Session

from handlers.text_commands import commands
import handlers.utils as utils

router = Router()

@router.callback_query(F.data == commands.my_subscriptions)
async def get_my_locations(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=commands.add_subscription, callback_data=commands.add_subscription))
    builder.row(InlineKeyboardButton(text='Обратно в меню', callback_data=commands.get_menu))
    await callback.message.answer("ваши подписки на погоду", reply_markup=builder.as_markup())
    await types.Message.delete(callback.message)


class AddSubscription(StatesGroup):
    choosing_location = State()
    choosing_detail_type = State()
    choosing_send_time = State()
    choosing_interval = State()


@router.callback_query(
        StateFilter(None),
        F.data == commands.add_subscription
        )
async def add_subscription(callback: types.CallbackQuery, state: FSMContext):
    user_locations = None
    user_id = callback.from_user.id
    async with Session() as session:
        user_locations = await utils.get_user_locations(user_id, session)
    if (not user_locations) or len(user_locations) == 0:
        await callback.message.answer(
            text=(
                'Похоже вы пока не добавили локации\n'
                'Это необходимо для подписки на погоду')
            )
        return
    builder = InlineKeyboardBuilder()
    for location in user_locations:
        builder.row(InlineKeyboardButton(
                text=location.name,
                callback_data=commands.get_subscription_location(location.name)
            ))
    await callback.message.answer(
        text='Выберите локацию',
        reply_markup=builder.as_markup()
    )
    await state.set_state(AddSubscription.choosing_location)


@router.callback_query(
        StateFilter(AddSubscription.choose_location),
        F.data.contains(commands.get_subscription_location(''))
        )
async def choose_location(callback: types.CallbackQuery, state: FSMContext):
    command = commands.get_subscription_location('')
    data = callback.data
    location_name = data[data.find(command) + len(command):]
    user_id = callback.from_user.id
    location = None
    async with Session() as session:
        location = await utils.check_location_exists(user_id, location_name, session)

    await state.update_data(location_id=location.id)
    await state.set_state(AddSubscription.choosing_detail_type)

    builder = InlineKeyboardBuilder()
    for detail_type_alias, detail_type in commands.detail_types:
        builder.row(InlineKeyboardButton(
            text=detail_type_alias,
            callback_data=commands.get_detail_type(detail_type)
        ))

    await callback.message.answer(
        text='Выберите тип отчета о погоде',
        reply_markup=builder.as_markup()
    )

    await types.Message.delete(callback.message)
    
@router.callback_query(
    StateFilter(AddSubscription.choosing_detail_type),
    F.data.contains(commands.get_detail_type(''))
)
async def choose_detail_type(callback: types.CallbackQuery, state: FSMContext):
    command = commands.get_detail_type('')
    data = callback.data
    detail_type = data[data.find(command) + len(command):]

    await state.update_data(detail_type=detail_type)
    await state.set_state(AddSubscription.choosing_send_time)

    await callback.message.answer(
        text=(
            'Выберите когда прислать первый отчет\n'
            f'Необходим формат времени {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'
            'Пришлите боту время в этом формате'
        )
    )

    await types.Message.delete(callback.message)

@router.message(
    StateFilter(AddSubscription.choosing_send_time)
)
async def choose_send_time(message: types.Message, state: FSMContext):
    time_to_send = message.text
    await state.update_data(next_event_time=time_to_send)
    await state.set_state(AddSubscription.choosing_interval)

    kb = [
        [KeyboardButton(text=24), KeyboardButton(text=72), KeyboardButton(text=168)]
    ]

    await message.answer(
        text=(
            'Выберите или напишите сами интервал в часах между сообщениями',
            'Пример: 72 будет значить каждые 3 дня, a 168 раз в неделю'
        ),
        reply_markup=ReplyKeyboardMarkup(keyboard=kb, one_time_keyboard=True, resize_keyboard=True)
    )

@router.message(
    StateFilter(AddSubscription.choosing_interval)
)
async def choose_interval(message: types.Message, state: FSMContext):
    num = message.text
    error_text = None
    if not num.isdecimal():
        error_text = 'Похоже вы ввели не число'
    num = int(num)
    if num < 1 or num > 168:
        error_text = 'Число должно быть в пределах от 1 до 168'
    
    if error_text:
        await message.answer(text=error_text)
        return
    
    data = await state.get_data()
    subscription = {
        'location_id': int(data['location_id']),
        'detail_type': data['detail_type'],
        'next_event_time': datetime.fromisoformat(data['next_event_time']),
        'period': num
    }
    subscription = None
    async with Session() as session:
        subscription = await utils.create_subscription(subscription, session)
    await message.answer(text='Подписка успешно создана')
    await state.set_state(None)
