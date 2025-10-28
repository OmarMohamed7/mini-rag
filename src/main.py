from fastapi import FastAPI
import uvicorn
from routes import base, data, nlp
from helpers.config import get_config
from contextlib import asynccontextmanager

from stores.llm import LLMFactory
from stores.llm.templates.template_parser import TemplateParser
from stores.vectordb import VectorDBProviderFactory
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("App started")
    app.state.app_config = get_config()

    postgres_username = app.state.app_config.POSTGRES_USERNAME
    postgres_password = app.state.app_config.POSTGRES_PASSWORD
    postgres_host = app.state.app_config.POSTGRES_HOST
    postgres_port = app.state.app_config.POSTGRES_PORT
    postgres_main_database = app.state.app_config.POSTGRES_MAIN_DATABASE

    postgres_conn_string = f"postgresql+psycopg://{postgres_username}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_main_database}"
    app.state.db_engine = create_async_engine(postgres_conn_string)
    app.state.db_client = sessionmaker(
        app.state.db_engine, expire_on_commit=False, class_=AsyncSession
    )

    # Initialize LLM factory
    llm_factory = LLMFactory(app.state.app_config)

    # Initialize generation client
    app.state.genration_client = llm_factory.get_llm(
        app.state.app_config.GENERATION_BACKEND
    )
    app.state.genration_client.set_generation_model(
        app.state.app_config.GENERATION_MODEL_ID
    )

    # Initialize embedding client
    app.state.embedding_client = llm_factory.get_llm(
        provider=app.state.app_config.EMBEDDING_BACKEND
    )
    app.state.embedding_client.set_embedding_model(
        model_id=app.state.app_config.EMBEDDING_MODEL_ID,
        embedding_size=app.state.app_config.EMBEDDING_MODEL_SIZE,
    )

    vector_db_factory = VectorDBProviderFactory(app.state.app_config)
    app.state.vector_db_client = vector_db_factory.create_vector_db(
        app.state.app_config.VECTOR_DB_BACKEND
    )

    app.state.template_parser = TemplateParser(
        locale=app.state.app_config.DEFAULT_LOCALE
    )

    app.state.vector_db_client.connect()

    yield
    # Shutdown logic
    print("App shutting down")
    await app.state.db_engine.dispose()
    app.state.vector_db_client.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(base.router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
