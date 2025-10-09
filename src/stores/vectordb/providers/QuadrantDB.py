from stores.vectordb import VectorDBInterface
from qdrant_client import QdrantClient, models
import logging

from stores.vectordb.VectorDBEnums import DistanceMethodsEnums


class QdrantDBProvider(VectorDBInterface):
    def __init__(
        self,
        db_path: str,
        distance_method: DistanceMethodsEnums = DistanceMethodsEnums.DOT,
    ):
        self.db_path = db_path
        self.client: QdrantClient = None
        self.distance_method = distance_method.value

        self.logger = logging.getLogger(__name__)

    def connect(self):
        if self.client:
            return

        self.client = QdrantClient(path=self.db_path, distance=self.distance_method)

    def disconnect(self):
        self.client.close()
        self.client = None

    def is_collection_exists(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)

    def get_all_collections(self) -> list[str]:
        return self.client.get_collections()

    def get_collection_details(self, collection_name: str) -> dict:
        return self.client.get_collection(collection_name=collection_name)

    def delete_collection(self, collection_name: str) -> bool:
        if not self.is_collection_exists(collection_name=collection_name):
            return False

        return self.client.delete_collection(collection_name=collection_name)

    def create_collection(
        self, collection_name: str, embedding_size: int, reset: bool = False
    ) -> bool:
        if reset and self.is_collection_exists(collection_name=collection_name):
            self.delete_collection(collection_name=collection_name)
            return True

        return self.client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=embedding_size, distance=self.distance_method
            ),
            timeout=10.0,
            force=reset,
        )

    def insert_one(
        self,
        collection_name: str,
        text: str,
        vector: list,
        metadata: dict = None,
        record_id: str = None,
    ) -> bool:
        try:
            if self.is_collection_exists(collection_name=collection_name):
                self.logger.error(f"Collection {collection_name} already exists")
                return False

            _ = self.client.upload_records(
                collection_name=collection_name,
                records=[
                    models.Record(
                        vector=vector,
                        payload={
                            "metadata": metadata,
                            "text": text,
                        },
                    )
                ],
            )
        except Exception as e:
            self.logger.error(f"Error inserting one record: {e}")
            return False

        return True

    def insert_many(
        self,
        collection_name: str,
        texts: list,
        vectors: list,
        metadata: list = None,
        record_ids: list = None,
        batch_size: int = 50,
    ) -> bool:
        try:
            if metadata is None:
                metadata = [None] * len(texts)

            if record_ids is None:
                record_ids = [None] * len(texts)

            for i in range(0, len(texts), batch_size):
                batch_end = i + batch_size
                batch_texts = texts[i:batch_end]
                batch_vectors = vectors[i:batch_end]
                batch_metadata = metadata[i:batch_end]
                batch_record = [
                    models.Record(
                        vector=batch_vectors[x],
                        payload={
                            "metadata": batch_metadata[x],
                            "text": batch_texts[x],
                        },
                    )
                    for x in range(0, len(batch_texts))
                ]

                _ = self.client.upload_records(
                    collection_name=collection_name,
                    records=batch_record,
                )
        except Exception as e:
            self.logger.error(f"Error inserting many records: {e}")
            return False

        return True

    def search_by_vector(
        self,
        collection_name: str,
        vector: list,
        limit: int = 10,
    ) -> list[dict]:
        try:
            return self.client.search(
                collection_name=collection_name, query_vector=vector, limit=limit
            )
        except Exception as e:
            self.logger.error(f"Error searching by vector: {e}")
            return []
