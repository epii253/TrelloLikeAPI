import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_env_file = ".env" if os.path.exists(".env") else ".env.example"

class Settings(BaseSettings):
    DATABASE_HOST: str | None = Field(default=None, max_length=100)
    DATABASE_USER: str = Field(max_length=128)
    DATABASE_PORT: int | None = Field(default=None)
    DATABASE_NAME: str = Field(min_length=1, max_length=30)
    POSTGRES_PASSWORD: str | None = Field(default=None, min_length=0, max_length=100)
    DATABASE_URL: str = Field()

    EXTERNAL_DATABASE_PORT: int = Field(le=8196)

    SECRET_KEY: str = Field(max_length=100)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(ge=1, le=60 * 24 * 30)
    ALGORITHM: str = Field(max_length=30)

    model_config = SettingsConfigDict(env_file=_env_file, env_file_encoding="utf-8")

env_settings: Settings = Settings()
