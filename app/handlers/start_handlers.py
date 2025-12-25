""" | Файл с основной задачей бота: выдачей интерсных вопросов пользователю | """

# Для работы с ботом
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
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
async def start_handler(message: Message, state: FSMContext):
    """Хэндлер для команды /start
    """    
    # Проверяем пользователя в бд
    user = Database.User.read(message.from_user.id)
    if not user: 
        Database.User.create(id= message.from_user.id, username= message.from_user.username)

    await state.clear()  
    await message.answer(StartMessages.START, reply_markup=start_keyboard().as_markup())

@router.callback_query(StartCallbackFactory.filter(F.action == StartActions.TASK))
async def random_question_handler(callback: CallbackQuery):
    """Обработчик для кнопки "Вопрос"
    """    
    # Получаем все задачи из базы
    all_tasks = Database.Task.read_all()
    if not all_tasks:
        return await callback.message.edit_text(StartMessages.NO_TASKS)

    # Выбираем случайную задачу
    random_task = random.choice(all_tasks)

    # Обновляем сообщение с задачей
    await callback.message.edit_text(
        StartMessages.TASK.value.format(
            category= random_task.category, 
            text= random_task.text
        ), 
        reply_markup=start_keyboard().as_markup()
    )

@router.callback_query(StartCallbackFactory.filter(F.action == StartActions.CHANCE))
async def random_chance_handler(callback: CallbackQuery):
    """Обработчик для кнопки "Шанс"
    """    
    # Получаем все шансы из базы
    all_chances = Database.Chances.read_all()
    if not all_chances:
        return await callback.message.edit_text(StartMessages.NO_CHANCES)

    # Выбираем случайный шанс
    random_chance = random.choice(all_chances)

    # Обновляем сообщение с шансом
    await callback.message.edit_text(
        StartMessages.CHANCE.value.format(
            category= random_chance.category, 
            text= random_chance.text
        ), 
        reply_markup=start_keyboard().as_markup()
    )