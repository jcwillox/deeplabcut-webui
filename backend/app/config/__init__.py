from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    projects: str = "backend/tests/testdata"
    frame_format: str = "img{:04}.png"

    class Config:
        env_file = ".env"
        env_prefix = "dlc_"


@lru_cache()
def get_settings():
    return Settings()
