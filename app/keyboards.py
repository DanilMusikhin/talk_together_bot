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

def pagination_keyboard(action, current_page, total_records, records_per_page=5):
    """Создаёт клавиатуру для переключения страниц.

    Args:
        action (str): Действие (например, READ).
        current_page (int): Текущая страница.
        total_records (int): Общее количество записей.
        records_per_page (int, optional): Количество записей на странице. По умолчанию 5.

    Returns:
        InlineKeyboardBuilder: Клавиатура с кнопками для переключения страниц.
    """
    keyboard = InlineKeyboardBuilder()
    if current_page > 0:
        keyboard.button(
            text="<",
            callback_data=DatabaseCallbackFactory(
                action=action, read_page=current_page - 1
            ),
        )
    if (current_page + 1) * records_per_page < total_records:
        keyboard.button(
            text=">",
            callback_data=DatabaseCallbackFactory(
                action=action, read_page=current_page + 1
            ),
        )
    return keyboard