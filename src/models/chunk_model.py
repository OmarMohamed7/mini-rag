from models.base_data_model import BaseDataModel
from models.db_schemas.data_chunk_schema import DataChunkSchema
from models.enums.database_enum import DatabaseEnum
from pymongo import InsertOne


class ChunkModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection = self.db_client[DatabaseEnum.DATA_CHUNK.value]

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DatabaseEnum.DATA_CHUNK.value not in all_collections:
            self.collection = self.db_client[DatabaseEnum.DATA_CHUNK.value]
            await self.collection.create_indexes(DataChunkSchema.get_indexes())

    def create_chunk(self, chunk: DataChunkSchema):
        return self.collection.insert_one(
            chunk.model_dump(by_alias=True, exclude_none=True)
        )

    def get_chunck(self, chunk_id: str):
        return self.collection.find_one({"chunk_id": chunk_id})

    async def insert_chunks(self, chunks: list[DataChunkSchema], batch_size: int = 100):
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]

            operations = [InsertOne(chunk.model_dump()) for chunk in batch]
            self.collection.bulk_write(operations)

        return len(chunks)

    async def delete_chunk_by_file_id(self, file_id: str):
        result = await self.collection.delete_many({"file_id": file_id})
        return result.deleted_count
