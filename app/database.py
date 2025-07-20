""" | Файл настройки базы данных | """

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from datetime import datetime
import logging

DATABASE_URL = "sqlite:///talk_together_bot.db"

engine = create_engine(DATABASE_URL)
local_session = sessionmaker(bind=engine)
base = declarative_base()


class Database:
    class __Base:
        __abstract__ = True

        id = Column(Integer, primary_key=True, index=True)
        created_at = Column(DateTime, nullable=False, default=datetime.now)

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
    logging.info("База данных и таблицы успешно созданы")