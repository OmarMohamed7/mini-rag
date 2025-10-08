from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str
    FILE_ALLOWED_EXTENSTIONS: list[str]
    FILE_MAX_SIZE: int
    FILE_CHUNK_DEFAULT_SIZE: int

    MONGODB_URL: str
    MONGO_COLLECTION: str

    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    OPENAI_API_KEY: str
    OPENAI_API_URL: str
    COHERE_API_KEY: str

    OPENAI_GENERATION_MODEL: str
    OPENAI_EMBEDDING_MODEL: str
    EMBEDDING_MODEL_SIZE: int

    COHERE_GENERATION_MODEL: int
    GENERATION_DEFAULT_MAX_TOKENS: int
    GENERATION_DEFAULT_TEMPERATURE: float

    model_config = SettingsConfigDict(env_file=".env")


def get_config():
    return Config()
