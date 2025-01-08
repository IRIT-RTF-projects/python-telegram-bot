import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import config
from handlers import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config['token'])

dp = Dispatcher()

dp.include_routers(
    main_menu,
    locations,
    subscriptions,
    weather,
    help
)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())