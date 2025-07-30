""" | Файл для получения различных клавиатур бота | """

# aiogram инлайн клавиатура 
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Фабрика для создания колбэков
from app.callback_factories import DatabaseCallbackFactory, DatabaseActions

def database_actions_keyboard() -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    kb.button(text= "Прочитать", callback_data= DatabaseCallbackFactory(action= DatabaseActions.READ))
    kb.button(text= "Добавить", callback_data= DatabaseCallbackFactory(action= DatabaseActions.CREATE))
    kb.button(text= "Обновить", callback_data= DatabaseCallbackFactory(action= DatabaseActions.UPDATE))
    kb.button(text= "Удалить", callback_data= DatabaseCallbackFactory(action= DatabaseActions.DELETE))
    kb.adjust(2, 2) # Размещает кнопки в 2 ряда по 2 кнопки
    return kb