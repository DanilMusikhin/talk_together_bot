""" / Файл обработки CRUD запросов к базе данных / """

# Для работы с тг
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import BaseFilter, Command
from aiogram.fsm.context import FSMContext
# Логирование
import logging

# Для работы с базой данных
from app.database import Database
# Конфиг для получения id администратора
from config.config_reader import config
# Диалоги
from app.messages import DatabaseMessages
# Клавиатуры
from app.keyboards import database_actions_keyboard
# Фабрика колбэков
from app.callback_factories import DatabaseCallbackFactory, DatabaseActions


"""
    Перменные для работы
"""
logger = logging.getLogger(__name__)
router = Router()



"""
    Фильтры
"""
class IsCreatorFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id == config.id_creator.get_secret_value():
            message.answer(DatabaseMessages.NO_RULES)

"""
    Хэндлеры
"""
""" Начало работы с базой данных """
@router.message(Command("questions"))
async def questions_handler(message: Message, state: FSMContext):
    await state.clear()
    kb = database_actions_keyboard()
    await message.answer(DatabaseMessages.START, reply_markup=kb.as_markup())
    logger.info(f"Пользователь {message.from_user.id} запросил действия с базой данных")

""" CREATE"""
@router.callback_query(DatabaseCallbackFactory.filter(F.action == DatabaseActions.CREATE))
async def create_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(DatabaseMessages.CREATE)