""" / Файл обработки SQL запросов / """

# Для работы с тг
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
# Логирование
import logging


# Для работы с бд
from app.database import engine
# Диалоги
from app.messages import SQLMessages
# Состояния FSM
from app.states import DatabaseStates
# Фильтры
from app.filters import IsAdminFilter
# Для SQL выражений
from sqlalchemy import text


"""
    Переменные для работы
"""
logger = logging.getLogger(__name__)
router = Router()


"""
    Обработчики
"""
""" Начало работы с SQL скриптами """
@router.message(Command("sql"), IsAdminFilter())
async def sql_handler(message: Message, state: FSMContext):
    """ Обработчик команды /sql для начала работы с SQL скриптами """
    await state.clear()

    # Получаем список таблиц из базы данных
    try:
        with engine.connect() as connection:
            # Для SQLite
            result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = [row[0] for row in result.fetchall()]
            tables_list = ", ".join(tables)
    except Exception as e:
        logger.error(f"Ошибка при получении списка таблиц: {e}")
        tables_list = "Ошибка при получении списка таблиц"

    await message.answer(SQLMessages.START.value.format(tables=tables_list))
    await state.set_state(DatabaseStates.SQL)


""" Выполнение SQL скрипта """
@router.message(DatabaseStates.SQL, IsAdminFilter())
async def sql_execute_handler(message: Message, state: FSMContext): 
    """ Получаем SQL-скрипт и пытаемся выполнить его"""
    sql_script = message.text
    logger.info(f"Пользователь {message.from_user.username} запросил выполнение SQL скрипта: {sql_script}")

    try:
        # Используем sessionmaker, как в остальных частях кода
        from app.database import local_session
        
        session = local_session()

        try: 
            result = session.execute(text(sql_script))
            
            # Пытаемся получить результаты
            try: 
                # Используем mappings() для получения результатов как словарей
                rows = result.mappings().fetchall()
                
                if rows:
                    columns = list(rows[0].keys())
                    result_text = "\t".join(columns) + "\n"
                    result_text += "-" * 50 + "\n"
                    for row in rows:
                        result_text += "\t".join(str(val) if val is not None else "NULL" for val in row.values()) + "\n"
                        
                    session.commit()
                    await message.answer(
                        SQLMessages.SUCCESS.value + "\n" + SQLMessages.RESULT.value.format(result=result_text)
                    )
                else:
                    # Если результатов нет (пустая таблица или не SELECT запрос)
                    session.commit()
                    await message.answer(SQLMessages.SUCCESS.value + "\n" + SQLMessages.NO_RESULT.value)

            except Exception as fetch_error:
                # Если это был НЕ SELECT запрос (INSERT, UPDATE, DELETE и т.д.)
                session.commit()
                await message.answer(SQLMessages.SUCCESS.value)

        finally:
            session.close()
    
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Ошибка при выполнении SQL скрипта от пользователя {message.from_user.id}: {error_msg}")
        await message.answer(SQLMessages.ERROR.value.format(error=error_msg))