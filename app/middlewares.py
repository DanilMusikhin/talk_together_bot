""" | Файл для мидварей | """

# Для создания мидварей
from aiogram import types
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Any, Callable, Dict, Awaitable


class CallbackResponseMiddleware(BaseMiddleware):
    """Outer-мидварь, чтобы был ответ на колбэки (чтобы пользователь видел, что запрос обрабатывается)

    Args:
        BaseMiddleware (_type_): Базовый класс мидварей
    """    
    async def __call__(
        self, 
        handler: Callable[[types.CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject, 
        data: Dict[str, Any]
    ) -> Any:
        await event.answer()
        return await handler(event, data)