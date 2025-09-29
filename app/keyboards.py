""" | Файл для получения различных клавиатур бота | """

# aiogram инлайн клавиатура 
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Фабрика для создания колбэков
from app.callback_factories import DatabaseCallbackFactory, DatabaseActions, DatabaseTable, StartCallbackFactory, StartActions

def database_actions_keyboard(table: DatabaseTable) -> InlineKeyboardBuilder:
    """Создаёт клавиатуру для действий с базой данных.

    Args:
        table: Тип таблицы (DatabaseTable.QUESTION или DatabaseTable.USER)

    Returns:
        InlineKeyboardBuilder: Клавиатура с кнопками для действий с базой данных.
    """    
    kb = InlineKeyboardBuilder()

    if (table == DatabaseTable.QUESTION):
        kb.button(text= "Прочитать", callback_data= DatabaseCallbackFactory(table= table, action= DatabaseActions.READ))
        kb.button(text= "Добавить", callback_data= DatabaseCallbackFactory(table= table, action= DatabaseActions.CREATE))
        kb.button(text= "Обновить", callback_data= DatabaseCallbackFactory(table= table, action= DatabaseActions.UPDATE))
        kb.button(text= "Удалить", callback_data= DatabaseCallbackFactory(table= table, action= DatabaseActions.DELETE))
        kb.adjust(2, 2) # Размещает кнопки в 2 ряда по 2 кнопки
    elif (table == DatabaseTable.USER):
        kb.button(text= "Прочитать", callback_data= DatabaseCallbackFactory(table= table, action= DatabaseActions.READ))
        kb.button(text="Количество", callback_data=DatabaseCallbackFactory(table= table, action=DatabaseActions.COUNT))
        kb.adjust(2)  # Размещает кнопки в 1 ряд по 2 кнопки

    return kb

def pagination_keyboard(table, action, current_page, total_records, records_per_page=5):
    """Создаёт клавиатуру для переключения страниц.

    Args:
        table: Тип таблицы
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
                table=table, action=action, read_page=current_page - 1
            ),
        )
    if (current_page + 1) * records_per_page < total_records:
        keyboard.button(
            text=">",
            callback_data=DatabaseCallbackFactory(
                table=table, action=action, read_page=current_page + 1
            ),
        )
    return keyboard

def start_keyboard():
    """Создаёт клавиатуру для стартового экрана.

    Returns:
        InlineKeyboardBuilder: Клавиатура с кнопками для стартового экрана.
    """
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Вопрос",
        callback_data=StartCallbackFactory(action=StartActions.QUESTION)
    )
    return kb