""" | Файл с состояниями | """

# Модули для управления состояниями
from aiogram.fsm.state import State, StateGroup

# Состояния для работы с базой данных database_handlers.py
class DatabaseStates(StateGroup):
    create = State()  # Состояние создания
    update = State()  # Состояние обновления
    delete = State()  # Состояние удаления