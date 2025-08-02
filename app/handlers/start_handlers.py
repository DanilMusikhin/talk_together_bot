""" | Файл с основной задачей бота: выдачей интерсных вопросов пользователю | """

# Для работы с ботом
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
# Для случайного выбора вопроса
import random
# Лоигрование
import logging

# Для работы с базой данных
from app.database import Database
# Сообщения
from app.messages import StartMessages
# Фабрика колбэков
from app.callback_factories import StartCallbackFactory, StartActions
# Клавиатуры
from app.keyboards import start_keyboard

"""
    Переменные для работы
"""
router = Router()
logger = logging.getLogger(__name__)


"""
    Хэндлеры
"""
@router.message(Command("start"))
async def start_handler(message: Message):
    """Хэндлер для команды /start
    """    
    await message.answer(StartMessages.START, reply_markup=start_keyboard().as_markup())

@router.callback_query(StartCallbackFactory.filter(F.action == StartActions.QUESTION))
async def random_question_handler(callback: CallbackQuery):
    """Обработчик для кнопки "Вопрос"
    """    
    # Получаем все вопросы из базы
    all_questions = Database.Question.read_all()
    if not all_questions:
        return await callback.message.edit_text(StartMessages.NO_QUESTIONS)

    # Выбираем случайный вопрос
    random_question = random.choice(all_questions)

    # Обновляем сообщение с вопросом
    await callback.message.edit_text(
        StartMessages.QUESTION.value.format(
            category= random_question.category, 
            text= random_question.text
        ), 
        reply_markup=start_keyboard().as_markup()
    )