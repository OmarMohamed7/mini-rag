from fastapi import FastAPI
import uvicorn
from routes import base, data, nlp
from helpers.config import get_config
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager

from stores.llm import LLMFactory
from stores.vectordb import VectorDBProviderFactory


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("App started")
    app.state.app_config = get_config()
    app.state.mongo_conn = AsyncIOMotorClient(app.state.app_config.MONGODB_URL)
    app.state.mongo_db = app.state.mongo_conn[app.state.app_config.MONGO_COLLECTION]

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

    app.state.vector_db_client.connect()

    yield
    # Shutdown logic
    print("App shutting down")
    app.state.mongo_conn.close()
    app.state.vector_db_client.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(base.router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
