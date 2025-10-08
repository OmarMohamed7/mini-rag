from stores.vectordb import VectorDBEnums
from stores.vectordb.providers import PineconeProvider, QdrantProvider
from abc import ABC, abstractmethod
from typing import List


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
    def get_all_collections(self) -> List[str]:
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
        vector: List,
        metadata: dict = None,
        record_id: str = None,
    ) -> bool:
        pass

    @abstractmethod
    def insert_many(
        self,
        collection_name: str,
        texts: List,
        vectors: List,
        metadata: List = None,
        record_ids: List = None,
        batch_size: int = 50,
    ) -> bool:
        pass

    @abstractmethod
    def search_by_vector(
        self,
        collection_name: str,
        vector: List,
        limit: int = 10,
    ) -> List[dict]:
        pass
