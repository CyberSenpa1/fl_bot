import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from handler.start import start_router
from db.users import init_db

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("TOKEN")

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()




async def main() -> None:

    await init_db()
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp.include_router(start_router) # Подключение роутера


    # And the run events dispatching
    await dp.start_polling(bot)
    await print("Запуск")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    # Проверка ci/cd