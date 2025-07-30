""" | Файл для управления колбэками в других файлах | """

# Модуль для управление данными колбэков
from aiogram.filters.callback_data import CallbackData
# Логировние
import logging
# Подключение Enum
from enum import Enum


logger = logging.getLogger(__name__)

class DatabaseActions(Enum):
    READ = "read"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

class DatabaseCallbackFactory(CallbackData, prefix='db'):
    """Класс для управления колбэками базы данных в handlers/database.py

    Args:
        CallbackData (_type_): наследуется класс данных колбэков
        prefix (str, optional): для различий разных колбэков
    """
    action: DatabaseActions
    read_page: int = 0