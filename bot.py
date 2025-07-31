""" | Файл настроки бота | """

# Библиотеки
from aiogram import Bot, Dispatcher, types, BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

import logging
import asyncio
from typing import Any, Callable, Dict, Awaitable

# Конфиг
from config.config_reader import config
# Обработчики
from app.handlers import database_handlers
# БД
from app.database import init_db
# Мидварь
from app.middlewares import CallbackResponseMiddleware


logger = logging.getLogger(__name__)

async def main():
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    logger.info("Логирование настроено")

    # Инициализация базы данных
    init_db()

    # Инициализация бота
    bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode= ParseMode.MARKDOWN))
    dp = Dispatcher(storage= MemoryStorage())

    # Установка команд
    commands = [
        types.BotCommand(command="/start", description="Запустить бота"),
    ]
    await bot.set_my_commands(commands)

    # Включение обработчиков и мидварей
    dp.callback_query.middleware(CallbackResponseMiddleware())
    dp.include_router(
        database_handlers.router,
    )

    # Начало работы бота
    logger.info("Бот запущен")
    await dp.start_polling(bot, allowed_updates=["message", "inline_query", "chat_member", "my_chat_member", "callback_query"])

if __name__ == "__main__":
    asyncio.run(main())