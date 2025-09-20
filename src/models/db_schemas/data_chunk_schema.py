from operator import gt
from pydantic import Field
from pymongo import IndexModel

from models.db_schemas.base_schema import BaseSchema


class DataChunkSchema(BaseSchema):
    project_id: str = Field(..., min_length=1)
    file_id: str = Field(..., min_length=1)
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict = Field(..., min_length=1)
    chunk_order: int = Field(..., gt=0)

    @classmethod
    def get_indexes(cls):
        return [
            IndexModel(
                [("project_id", 1)], unique=False, name="project_chunk_id_index"
            ),
        ]
