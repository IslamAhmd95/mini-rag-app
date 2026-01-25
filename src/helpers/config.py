from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # We use Field(default=...) to tell the type checker: 
    # "Don't worry, a value will be provided" (via the .env file)
    APP_NAME: str = Field(default=...)
    APP_VERSION: str = Field(default=...)
    FILE_ALLOWED_TYPES: list = Field(default=...)
    FILE_MAX_SIZE: int = Field(default=...)
    FILE_DEFAULT_CHUNK_SIZE: int = Field(default=...)
    MONGODB_URL: str = Field(default=...)
    MONGODB_DATABASE: str = Field(default=...)

    model_config = SettingsConfigDict(env_file='.env')

def get_settings():
    return Settings()