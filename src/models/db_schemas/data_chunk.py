from operator import gt
from pydantic import Field

from models.db_schemas.base_schema_model import BaseSchemaModel


class DataChunk(BaseSchemaModel):
    project_id: str = Field(..., min_length=1)
    file_id: str = Field(..., min_length=1)
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict = Field(..., min_length=1)
    chunk_order: int = Field(..., gt=0)
