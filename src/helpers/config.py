from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str
    FILE_ALLOWED_EXTENSTIONS: list[str]
    FILE_MAX_SIZE: int

    model_config = SettingsConfigDict(env_file=".env")


def get_config():
    return Config()
