import asyncio
import logging

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import config
import handlers as h
from subscription_manager.send_reports import send_subscribtion_reports

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config['token'])

dp = Dispatcher()

dp.include_routers(
    h.main_menu,
    h.locations,
    h.subscriptions,
    h.weather,
    h.help
)


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_subscribtion_reports, "interval", seconds=60, args=(bot,))
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
