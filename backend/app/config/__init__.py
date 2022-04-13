from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    projects: str

    class Config:
        env_file = ".env"
        env_prefix = "dlc_"


@lru_cache()
def get_settings():
    return Settings()
