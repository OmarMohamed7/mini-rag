from pydantic import Field
from models.db_schemas.base_schema import BaseSchema


class RetrieveDocumentsSchema(BaseSchema):
    text: str = Field(..., min_length=1)
    score: float
