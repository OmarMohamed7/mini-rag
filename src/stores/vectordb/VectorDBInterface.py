from abc import ABC, abstractmethod

from models.db_schemas.retrieve_documents_schema import RetrieveDocumentsSchema


class VectorDBInterface(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def is_collection_exists(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def get_all_collections(self) -> list[str]:
        pass

    @abstractmethod
    def get_collection_details(self, collection_name: str) -> dict:
        pass

    @abstractmethod
    def create_collection(
        self, collection_name: str, embedding_size: int, reset: bool = False
    ) -> bool:
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def insert_one(
        self,
        collection_name: str,
        text: str,
        vector: list,
        metadata: dict = None,
        record_id: str = None,
    ) -> bool:
        pass

    @abstractmethod
    def insert_many(
        self,
        collection_name: str,
        texts: list,
        vectors: list,
        metadata: list = None,
        record_ids: list = None,
        batch_size: int = 50,
    ) -> bool:
        pass

    @abstractmethod
    def search_by_vector(
        self,
        collection_name: str,
        vector: list,
        limit: int = 10,
    ) -> list[RetrieveDocumentsSchema]:
        pass
