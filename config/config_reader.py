""" | Файл настроки бота | """

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Secret

SecretInt = Secret[int] # Создание типа SecretInt 

class Config(BaseSettings):
    bot_token: SecretStr
    id_owner: SecretInt

    model_config = SettingsConfigDict(env_file='config/config.env', env_file_encoding='utf-8')

config = Config()