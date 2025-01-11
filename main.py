import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import config
import handlers as h

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
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
