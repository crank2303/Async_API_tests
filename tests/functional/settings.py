import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

    ELASTIC_HOST = os.getenv("ELASTIC_HOST", "elasticsearch")
    ELASTIC_PORT = int(os.getenv("ELASTIC_PORT", "9200"))

    API_HOST = os.getenv("API_HOST", "movies_api")
    API_PORT = int(os.getenv("API_PORT", "8082"))

    es_url: str = os.environ.get("ES_URL", "elasticsearch:9200")
    redis_url: str = os.environ.get("REDIS_URL", "redis:6379")
    service_url: str = os.environ.get(
        "SERVICE_URL", "http://127.0.0.1:8082/api/v1"
    )

    class Config:
        env_file = ".env"


settings: Settings = Settings()
