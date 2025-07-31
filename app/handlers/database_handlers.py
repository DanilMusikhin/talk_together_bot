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
from app.messages import DatabaseMessages
# Клавиатуры
from app.keyboards import database_actions_keyboard
# Фабрика колбэков
from app.callback_factories import DatabaseCallbackFactory, DatabaseActions
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
    kb = database_actions_keyboard()
    await message.answer(DatabaseMessages.START, reply_markup=kb.as_markup())
    logger.info(f"Пользователь {message.from_user.id} запросил действия с базой данных")

""" CREATE"""
@router.callback_query(DatabaseCallbackFactory.filter(F.action == DatabaseActions.CREATE))
async def create_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(DatabaseMessages.CREATE)
    await state.set_state(DatabaseStates.CREATE)

@router.message(DatabaseStates.CREATE)
async def create_message_handler(message: Message, state: FSMContext):
    try:
        category, text = message.text.split("_", 1)
        Database.Question.create(category= category, text= text)
        await message.answer(DatabaseMessages.CREATE_SUCCESS)
    except Exception as e:
        await message.answer(DatabaseMessages.CREATE_ERROR)
        logger.error(f"Ошибка при создании вопроса: {e}")

""" UPDATE """
@router.callback_query(DatabaseCallbackFactory.filter(F.action == DatabaseActions.UPDATE))
async def update_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(DatabaseMessages.UPDATE)
    await state.set_state(DatabaseStates.UPDATE)

@router.message(DatabaseStates.UPDATE)
async def update_message_handler(message: Message, state: FSMContext):
    try:
        question_id, new_category, new_text = message.text.split("_", 2)
        question_id = int(question_id)
        updated_question = Database.Question.update(question_id, category=new_category, text=new_text)
        if updated_question:
            await message.answer(DatabaseMessages.UPDATE_SUCCESS)
        else:
            await message.answer(DatabaseMessages.UPDATE_NOT_FOUND)
    except ValueError:
        await message.answer(DatabaseMessages.UPDATE_ERROR)

""" DELETE """
@router.callback_query(DatabaseCallbackFactory.filter(F.action == DatabaseActions.DELETE))
async def delete_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(DatabaseMessages.DELETE)
    await state.set_state(DatabaseStates.DELETE)

@router.message(DatabaseStates.DELETE)
async def delete_message_handler(message: Message, state: FSMContext):
    try:
        question_id = int(message.text)
        deleted_question = Database.Question.delete(question_id)
        if deleted_question:
            await message.answer(DatabaseMessages.DELETE_SUCCESS)
        else:
            await message.answer(DatabaseMessages.DELETE_NOT_FOUND)
    except ValueError:
        await message.answer(DatabaseMessages.DELETE_ERROR)