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
from models.errors import ObjectNotFoundError

router = Router()

@router.callback_query(F.data == commands.my_subscriptions)
async def get_my_subscriptions(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    user_id = callback.from_user.id

    subscriptions = []
    async with Session() as session:
        subscriptions = await utils.get_user_subscriptions(user_id, session)
    
        for subscription in subscriptions:
            builder.row(
                InlineKeyboardButton(
                    text=f'{subscription.location.name} {subscription.next_event_time}',
                    callback_data=commands.get_subscription_info(str(subscription.id))
                )
            )

    builder.row(InlineKeyboardButton(text=commands.add_subscription, callback_data=commands.add_subscription))
    builder.row(InlineKeyboardButton(text='Обратно в меню', callback_data=commands.get_menu))

    await callback.message.answer("Ваши подписки на погоду", reply_markup=builder.as_markup())
    await types.Message.delete(callback.message)


@router.callback_query(
    F.data.contains(commands.get_subscription_info(''))
)
async def get_subscription_info(callback: types.CallbackQuery):
    command = commands.get_subscription_info('')
    data = callback.data
    subscription_id = data[data.find(command) + len(command):]

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Удалить подписку', callback_data= commands.delete_subscription(subscription_id)))
    builder.row(InlineKeyboardButton(text='Обратно в меню', callback_data=commands.get_menu))

    subscription = None
    location_name = None
    async with Session() as session:
        subscription = await utils.get_subscription_by_id(int(subscription_id), session)
        location_name = subscription.location.name
    
    subscription_detail_type = None
    for detail_type_alias, detail_type in commands.detail_types:
        if detail_type == subscription.detail_type:
            subscription_detail_type = detail_type_alias

    subscription_data = (
        f'Локация: {location_name}\n'
        f'Следующий отчет: {subscription.next_event_time}\n'
        f'Тип отчета: {subscription_detail_type}\n'
        f'Период между отчетами: {subscription.period} часов'
    )

    await callback.message.answer(text=subscription_data, reply_markup=builder.as_markup())
    await types.Message.delete(callback.message)

@router.callback_query(
    F.data.contains(commands.delete_subscription(''))
)
async def delete_subscription(callback: types.CallbackQuery):
    command = commands.delete_subscription("")
    data = callback.data
    subscription_id = data[data.find(command) + len(command):]
    async with Session() as session:
        try:
            await utils.delete_subscription(int(subscription_id), session)
        except ObjectNotFoundError:
            await callback.mesage.answer('хмм... Похоже эта подписка уже была удалена')
    await callback.message.answer('Подписка успешно удалена')

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
        StateFilter(AddSubscription.choosing_location),
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
            'Пришлите боту время в формате\n'
            f'`{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`'
        ), parse_mode='MarkdownV2'
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
        [KeyboardButton(text='24'), KeyboardButton(text='72'), KeyboardButton(text='168')]
    ]

    await message.answer(
        text=(
            'Выберите или напишите сами интервал в часах между сообщениями\n'
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
    subscription_data = {
        'location_id': int(data['location_id']),
        'detail_type': data['detail_type'],
        'next_event_time': datetime.fromisoformat(data['next_event_time']),
        'period': num
    }
    subscription = None
    async with Session() as session:
        subscription = await utils.create_subscription(subscription_data, session)
    await message.answer(text='Подписка успешно создана')
    await state.set_state(None)
