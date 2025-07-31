""" | Файл настройки базы данных | """

# Для работы с базой данных
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Для указания времени создания записи
from datetime import datetime
# Логирование
import logging

# Конфиг
from config.config_reader import config


# Настройка базы данных
logger = logging.getLogger(__name__)
engine = create_engine(config.database_url.get_secret_value())
local_session = sessionmaker(bind=engine)
base = declarative_base()


class Database:
    class __Base(base):
        __abstract__ = True

        id = Column(Integer, primary_key=True, index=True)
        timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

        @classmethod
        def create(cls, **kwargs):
            session = local_session()
            obj = cls(**kwargs)
            session.add(obj)
            session.commit()
            session.refresh(obj)
            session.close()
            return obj
        
        @classmethod
        def read(cls, obj_id):
            session = local_session()
            obj = session.query(cls).get(obj_id)
            session.close()
            return obj
        
        @classmethod
        def read_all(cls):
            session = local_session()
            objs = session.query(cls).all()
            session.close()
            return objs
        
        @classmethod
        def update(cls, obj_id, **kwargs):
            session = local_session()
            obj = session.query(cls).get(obj_id)
            if obj:
                for key, value in kwargs.items():
                    setattr(obj, key, value)
                obj.timestamp = datetime.utcnow() # обновляем время изменения
                session.commit()
            session.close()
            return obj
        
        @classmethod
        def delete(cls, obj_id):
            session = local_session()
            obj = session.query(cls).get(obj_id)
            if obj:
                session.delete(obj)
                session.commit()
            session.close()
            return obj
        
    class Question(__Base):
        __tablename__ = 'questions'

        category = Column(String, nullable=False)
        text = Column(String, nullable=False)


def init_db():
    base.metadata.create_all(bind=engine)
    logger.info("База данных и таблицы успешно созданы")