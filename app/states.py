""" | Файл с состояниями | """

# Модули для управления состояниями
from aiogram.fsm.state import State, StatesGroup

# Состояния для работы с базой данных database_handlers.py
class DatabaseStates(StatesGroup):
    CREATE = State()  # Состояние создания
    UPDATE = State()  # Состояние обновления
    DELETE = State()  # Состояние удаления
    SQL = State() # Состояние для отправки SQL скрипта