""" | Файл для фильтров | """

# Для создания фильтров
from aiogram.filters import BaseFilter
# Для отправки сообщений
from aiogram.types import Message
# Сообщения для отправки пользователю
from app.messages import DatabaseMessages
# Конфиг для получения id администратора
from config.config_reader import config



class IsAdminFilter(BaseFilter):
    """Фильтр для проверки прав администратора

    Args:
        BaseFilter (_type_): Базовый класс фильтра
    """    
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id in config.id_admins:
            return True
        await message.answer(DatabaseMessages.NO_RULES)
        return False