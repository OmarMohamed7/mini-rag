from operator import gt
from bson import ObjectId
from pydantic import Field
from pymongo import IndexModel

from models.db_schemas.base_schema import BaseSchema


class DataChunkSchema(BaseSchema):
    project_id: str = Field(..., min_length=1)
    file_id: ObjectId
    file_name: str = Field(..., min_length=1)
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict = Field(..., min_length=1)
    chunk_order: int = Field(..., gt=0)

    @classmethod
    def get_indexes(cls):
        return [
            IndexModel(
                [("project_id", 1)], unique=False, name="project_chunk_id_index"
            ),
            IndexModel([("file_id", 1)], unique=False, name="file_chunk_id_index"),
            IndexModel(
                [("file_name", 1)], unique=False, name="file_name_chunk_id_index"
            ),
        ]
