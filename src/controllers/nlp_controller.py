from controllers.base_controller import BaseController
from models.db_schemas.data_chunk_schema import DataChunkSchema
from models.db_schemas.project_schema import ProjectSchema
from routes.schema.nlp_schema import IndexPushRequestSchema
from stores.llm import LLMInterface
from stores.llm.LLMEnums import DocumentTypesEnums
from stores.vectordb import VectorDBInterface
import uuid


class NLPController(BaseController):
    def __init__(
        self,
        vector_db_client: VectorDBInterface,
        generation_client: LLMInterface,
        embedding_client: LLMInterface,
    ):
        super().__init__()
        self.vector_db_client = vector_db_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client

    def create_collection_name(self, project_id: str) -> str:
        return f"collection_{project_id}".strip().lower()

    def reset_vector_db_collection(self, project_id: str):
        collection_name = self.create_collection_name(project_id)
        return self.vector_db_client.delete_collection(collection_name=collection_name)

    def get_vector_db_collection_info(self, project_id: str):
        collection_name = self.create_collection_name(project_id)
        return self.vector_db_client.get_collection_details(
            collection_name=collection_name
        )

    def index_into_vector_db(
        self,
        project_id: str,
        chunks: list[DataChunkSchema],
        chunks_ids: list[str],
        reset: bool = False,
    ):
        collection_name = self.create_collection_name(project_id)

        texts = [chunk.chunk_text for chunk in chunks]
        metadata = [chunk.chunk_metadata for chunk in chunks]

        vectors = [
            self.embedding_client.embed_text(
                text=text, document_type=DocumentTypesEnums.DOCUMENT.value
            )
            for text in texts
        ]

        if not self.vector_db_client.is_collection_exists(collection_name):

            _ = self.vector_db_client.create_collection(
                collection_name=collection_name,
                embedding_size=self.embedding_client.embedding_size,
                reset=reset,
            )

        return self.vector_db_client.insert_many(
            collection_name=collection_name,
            texts=texts,
            vectors=vectors,
            metadata=metadata,
            record_ids=chunks_ids,
        )

    def search_project_index(
        self, project_id: str, text: str, limit: int = 10, offset: int = 0
    ):
        collection_name = self.create_collection_name(project_id)

        vector = self.embedding_client.embed_text(
            text=text, document_type=DocumentTypesEnums.QUERY.value
        )

        if not vector or len(vector) == 0:
            return False

        return self.vector_db_client.search_by_vector(
            collection_name=collection_name,
            vector=vector,
            limit=limit,
        )
