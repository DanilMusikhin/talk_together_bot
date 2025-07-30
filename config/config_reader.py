""" | Файл настроки бота | """

# Для создания кофига
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Secret
# Для создания списка id admins
from typing import List

class Config(BaseSettings):
    bot_token: SecretStr # Токен бота
    id_admins: List[int] # Список id администраторов
    database_url: SecretStr # URL базы данных

    model_config = SettingsConfigDict(env_file='config/config.env', env_file_encoding='utf-8')

config = Config()