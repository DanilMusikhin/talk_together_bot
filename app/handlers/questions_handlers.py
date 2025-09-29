""" / Файл обработки CRUD запросов к базе данных / """

# Для работы с тг
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
# Логирование
import logging

# Для работы с базой данных
from app.database import Database
# Диалоги
from app.messages import QuestionsMessages
# Клавиатуры
from app.keyboards import database_actions_keyboard, pagination_keyboard
# Фабрика колбэков
from app.callback_factories import DatabaseCallbackFactory, DatabaseActions, DatabaseTable
# Состояния
from app.states import DatabaseStates
# Фильтры
from app.filters import IsAdminFilter


"""
    Перменные для работы
"""
logger = logging.getLogger(__name__)
router = Router()


"""
    Хэндлеры
"""
""" Начало работы с базой данных """
@router.message(Command("questions"), IsAdminFilter())
async def questions_handler(message: Message, state: FSMContext):
    await state.clear()
    kb = database_actions_keyboard(DatabaseTable.QUESTION)
    await message.answer(QuestionsMessages.START, reply_markup=kb.as_markup())
    logger.info(f"Пользователь {message.from_user.id} запросил действия с базой данных")

""" CREATE"""
@router.callback_query(DatabaseCallbackFactory.filter(F.table == DatabaseTable.QUESTION and F.action == DatabaseActions.CREATE))
async def create_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(QuestionsMessages.CREATE)
    await state.set_state(DatabaseStates.CREATE)

@router.message(DatabaseStates.CREATE)
async def create_message_handler(message: Message, state: FSMContext):
    try:
        category, text = message.text.split("_", 1)
        Database.Question.create(category= category, text= text)
        await message.answer(QuestionsMessages.CREATE_SUCCESS)
    except ValueError:
        await message.answer(QuestionsMessages.CREATE_ERROR)
        logger.error(f"Ошибка при создании вопроса: {message.text}")

""" READ """
@router.callback_query(DatabaseCallbackFactory.filter(F.table == DatabaseTable.QUESTION), DatabaseCallbackFactory.filter(F.action == DatabaseActions.READ))
async def read_handler(callback: CallbackQuery, callback_data: DatabaseCallbackFactory):
    """Обработчик для чтения данных из базы по страницам.

    Args:
        callback (CallbackQuery): Объект колбэка.
        callback_data (DatabaseCallbackFactory): Данные колбэка для определения страницы.
    """
    try:
        # Устанавливаем количество записей на странице
        records_per_page = 5
        page = callback_data.read_page

        # Получаем все записи из таблицы
        all_questions = Database.Question.read_all()
        total_records = len(all_questions)

        if total_records == 0:
            return await callback.message.edit_text(QuestionsMessages.READ_EMPTY)

        # Вычисляем записи для текущей страницы
        start_index = page * records_per_page
        end_index = start_index + records_per_page
        page_records = all_questions[start_index:end_index]

        # Формируем текст ответа
        response = "\n".join(
            [f"{record.id}. [{record.category}] {record.text}" for record in page_records]
        )

        # Создаём клавиатуру для переключения страниц
        keyboard = pagination_keyboard(
            table=DatabaseTable.QUESTION,
            action=DatabaseActions.READ, 
            current_page=page, 
            total_records=total_records, 
            records_per_page=records_per_page
        )

        # Отправляем сообщение с данными и кнопками
        await callback.message.edit_text(response, reply_markup=keyboard.as_markup())
    except Exception as e:
        logger.error(f"Ошибка при чтении данных: {e}")
        await callback.message.edit_text(QuestionsMessages.READ_ERROR)

""" UPDATE """
@router.callback_query(DatabaseCallbackFactory.filter(F.table == DatabaseTable.QUESTION and F.action == DatabaseActions.UPDATE))
async def update_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(QuestionsMessages.UPDATE)
    await state.set_state(DatabaseStates.UPDATE)

@router.message(DatabaseStates.UPDATE)
async def update_message_handler(message: Message, state: FSMContext):
    try:
        question_id, new_category, new_text = message.text.split("_", 2)
        question_id = int(question_id)
        updated_question = Database.Question.update(question_id, category=new_category, text=new_text)
        if updated_question:
            await message.answer(QuestionsMessages.UPDATE_SUCCESS)
        else:
            await message.answer(QuestionsMessages.UPDATE_NOT_FOUND)
    except ValueError:
        await message.answer(QuestionsMessages.UPDATE_ERROR)
        logger.error(f"Ошибка при обновлении вопроса: {message.text}")

""" DELETE """
@router.callback_query(DatabaseCallbackFactory.filter(F.table == DatabaseTable.QUESTION and F.action == DatabaseActions.DELETE))
async def delete_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(QuestionsMessages.DELETE)
    await state.set_state(DatabaseStates.DELETE)

@router.message(DatabaseStates.DELETE)
async def delete_message_handler(message: Message, state: FSMContext):
    try:
        question_id = int(message.text)
        deleted_question = Database.Question.delete(question_id)
        if deleted_question:
            await message.answer(QuestionsMessages.DELETE_SUCCESS)
        else:
            await message.answer(QuestionsMessages.DELETE_NOT_FOUND)
    except ValueError:
        await message.answer(QuestionsMessages.DELETE_ERROR)
        logger.error(f"Ошибка при удалении вопроса: {message.text}")