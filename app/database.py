""" | Файл настройки базы данных | """

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import logging

DATABASE_URL = "sqlite:///talk_together_bot.db"

engine = create_engine(DATABASE_URL)
local_session = sessionmaker(bind=engine)
base = declarative_base()

class Question(base):
    __tablename__ = 'questions'
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    text = Column(String, nullable=False)


def init_db():
    base.metadata.create_all(bind=engine)
    logging.info("База данных и таблицы успешно созданы")