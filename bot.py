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

# БД
from app.database import init_db


# Outer-мидварь, чтобы был ответ на колбэки (чтобы пользователь видел, что запрос обрабатывается)
class CallbackResponseMiddleware(BaseMiddleware):
    async def __call__(
        self, 
        handler: Callable[[types.CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject, 
        data: Dict[str, Any]
    ) -> Any:
        await event.answer()
        return await super().__call__(handler, event, data)


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
    bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode= ParseMode.HTML))
    dp = Dispatcher(storage= MemoryStorage())

    # Установка команд
    commands = [
        types.BotCommand(command="/start", description="Запустить бота"),
    ]
    await bot.set_my_commands(commands)

    # Включение обработчиков и мидварей
    dp.callback_query.middleware(CallbackResponseMiddleware())
    # dp.include_router(
    #     # Здесь будут подключены обработчики
    # )   

    # Начало работы бота
    logger.info("Бот запущен")
    await dp.start_polling(bot, allowed_updates=["message", "inline_query", "chat_member", "my_chat_member", "callback_query"])

if __name__ == "__main__":
    asyncio.run(main())