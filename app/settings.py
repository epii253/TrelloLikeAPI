from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = Field()

    SECRET_KEY: str = Field(max_length=100)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(ge=1, le= 60*24*30)
    ALGORITHM: str = Field(max_length=30)

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

env_settings = Settings()
