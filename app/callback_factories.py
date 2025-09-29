""" | Файл для управления колбэками в других файлах | """

# Модуль для управление данными колбэков
from aiogram.filters.callback_data import CallbackData
# Логировние
import logging
# Подключение Enum
from enum import Enum


logger = logging.getLogger(__name__)


"""
    database_handlers.py
"""
class DatabaseTable(Enum):
    QUESTION = "question"
    USER = "user"

class DatabaseActions(Enum):
    READ = "read"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    COUNT = "count"

class DatabaseCallbackFactory(CallbackData, prefix='db'):
    table: DatabaseTable
    action: DatabaseActions
    read_page: int = 0

"""
    start_handlers.py
"""
class StartActions(Enum):
    QUESTION = "question"

class StartCallbackFactory(CallbackData, prefix="start"):
    action: StartActions