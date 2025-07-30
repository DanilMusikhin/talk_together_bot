from enum import Enum

class DatabaseMessages(Enum):
    NO_RULES = "У вас нет прав для работы с бд"
    START = "Выберите действие с таблицей Questions:"
    CREATE = "Пример отправки:\n`Мнение_Что ценишь в людях?`"