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
class DatabaseActions(Enum):
    READ = "read"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

class DatabaseCallbackFactory(CallbackData, prefix='db'):
    action: DatabaseActions
    read_page: int = 0

"""
    start_handlers.py
"""
class StartActions(Enum):
    QUESTION = "question"

class StartCallbackFactory(CallbackData, prefix="start"):
    action: StartActions