from pathlib import Path

from logging import config as logging_config
from pydantic import BaseSettings, Field

from core.logger import LOGGING


class Settings(BaseSettings):
    redis_host: str = Field('127.0.0.1', env='REDIS_HOST')
    redis_port: int = Field(6379, env='REDIS_PORT')
    project_name: str = Field('movies', env='PROJECT_NAME')
    elastic_host: str = Field('127.0.0.1', env='ELASTIC_HOST')
    elastic_port: int = Field(9200, env='ELASTIC_PORT')
    redis_cache_expire_seconds: int = Field(300, env='REDIS_CACHE_EXPIRE_SECONDS')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
logging_config.dictConfig(LOGGING)
