import asyncio
import logging
from aiogram import Dispatcher
from handlers import router
from bot_instance import bot  # Імпортуємо бот

async def main():
    logging.basicConfig(level=logging.INFO)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
