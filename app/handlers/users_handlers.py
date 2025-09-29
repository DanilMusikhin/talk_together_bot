# Для работы с тг
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
# Логирование
import logging

# Для работы с бд
from app.database import Database
# Диалоги 
from app.messages import UsersMessages
# Клавиатуры 
from app.keyboards import database_actions_keyboard, pagination_keyboard
# Фабрика колбэков
from app.callback_factories import DatabaseCallbackFactory, DatabaseActions, DatabaseTable
# Фильтры
from app.filters import IsAdminFilter


"""
    Переменные для работы
"""
logger = logging.getLogger(__name__)
router = Router()


"""
    Хэндрлеры
"""
""" Начало работы с пользователями """
@router.message(Command("users"), IsAdminFilter())
async def users_handler(message: Message, state: FSMContext):
    await state.clear()
    kb = database_actions_keyboard(DatabaseTable.USER)
    await message.answer(UsersMessages.START, reply_markup= kb.as_markup())

""" READ """
@router.callback_query(DatabaseCallbackFactory.filter(F.table == DatabaseTable.USER), DatabaseCallbackFactory.filter(F.action == DatabaseActions.READ))
async def read_users_handler(callback: CallbackQuery, callback_data: DatabaseCallbackFactory): 
    try:
        # Устанавливаем количество записей на странице
        records_per_page = 5
        page = callback_data.read_page

        # Получаем всех пользователей из таблицы
        all_users = Database.User.read_all()
        total_records = len(all_users)

        if total_records == 0:
            return await callback.message.edit_text(UsersMessages.READ_EMPTY)

        # Вычисляем записи для текущей страницы
        start_index = page * records_per_page
        end_index = start_index + records_per_page
        page_records = all_users[start_index:end_index]

        # Формируем текст ответа
        response = "\n".join(
            [f"{record.id} @{record.username} (регистр. {record.timestamp.strftime('%d.%m.%Y %H:%M')})" for record in page_records]
        )

        # Создаём клавиатуру для переключения страниц
        keyboard = pagination_keyboard(
            table=DatabaseTable.USER,
            action=DatabaseActions.READ, 
            current_page=page, 
            total_records=total_records, 
            records_per_page=records_per_page
        )

        # Отправляем сообщение с данными и кнопками
        await callback.message.edit_text(response, reply_markup=keyboard.as_markup())
    except Exception as e:
        logger.error(f"Ошибка при чтении пользователей: {e}")
        await callback.message.edit_text(UsersMessages.READ_ERROR)  


""" COUNT """
@router.callback_query(DatabaseCallbackFactory.filter(F.table == DatabaseTable.USER and F.action == DatabaseActions.COUNT))
async def count_users_handler(callback: CallbackQuery):
    try: 
        # Получаем всех пользователей из таблицы
        all_users = Database.User.read_all()
        total_count = len(all_users)

        # Отправляем сообщение с количеством
        await callback.message.edit_text(UsersMessages.COUNT_MESSAGE.value.format(count= total_count))
    except Exception as e:
        logger.error(f"Ошибка при подсчете пользователей: {e}")
        await callback.message.edit_text(UsersMessages.COUNT_ERROR)