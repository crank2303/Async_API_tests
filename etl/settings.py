"""Module with settings."""
import os
from pydantic import BaseSettings, Field


class PostgresSettings(BaseSettings):
    dbname: str = os.environ.get('POSTGRES_D', 'movies_database')
    user: str = os.environ.get('POSTGRES_USE', 'app')
    password: str = os.environ.get('POSTGRES_PASSWOR', '123qwe')
    host: str = os.environ.get('POSTGRES_HOS', '127.0.0.1')
    port: int = os.environ.get('POSTGRES_POR', '5433')
    options: str = os.environ.get('DB_OPTIONS')


class Settings(BaseSettings):
    last_state_key: str = os.environ.get('ETL_STATE_KEY')
    state_file_path: str = os.environ.get('ETL_STATE_STORAGE', 'ex.json')
    dsn: PostgresSettings = PostgresSettings()
    batch_size: int = os.environ.get('CHUNK_SIZE', 100)
    es_host: str = os.environ.get('ES_URL', 'http://127.0.0.1:9200')
    offset_counter: int = 0


settings = Settings()
settings.dsn.user = 'app'