from datetime import datetime, timedelta

from aiogram import Bot

from crud import subscription_crud
from models.db import Session
from weather_requests.weather import weather


async def send_subscribtion_reports(bot: Bot):
    async with Session() as session:
        subscriptions = await subscription_crud.get_all(session)

        now = datetime.now()

        for subscription in subscriptions:

            next_event_time = subscription.next_event_time

            if next_event_time > now:
                continue

            location = subscription.location
            user = subscription.location.user

            text = 'Отчет по подписке\n'

            text += await weather.get_weather_forecast(
                detail_type=subscription.detail_type,
                number_of_days=2,
                latitude=location.latitude,
                longitude=location.longitude
            )

            await bot.send_message(
                chat_id=user.chat_id,
                text=text
            )

            new_event_time = next_event_time + timedelta(hours=subscription.period)

            await subscription_crud.update(
                subscription.id,
                {"next_event_time": new_event_time},
                session,
            )
