from stores.vectordb import VectorDBEnums
from stores.vectordb.providers.QuadrantDB import QdrantDBProvider
from controllers.base_controller import BaseController


class VectorDBProviderFactory:
    def __init__(self, config: dict):
        self.base_controller = BaseController()
        self.config = config

    def create_vector_db(self, provider: str):
        if provider == VectorDBEnums.QDRANT.value:
            db_path = self.base_controller.get_database_path(
                database_name=self.config.VECTOR_DB_PATH
            )
            return QdrantDBProvider(
                db_path=db_path,
                distance_method=VectorDBEnums.DistanceMethodsEnums.COSINE,
            )

        raise ValueError(f"Invalid provider: {provider}")


# test comment
