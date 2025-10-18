from pydantic import BaseModel
from typing import Optional


class IndexPushRequestSchema(BaseModel):
    reset: Optional[int] = 0


class SearchRequestSchema(BaseModel):
    text: str
    limit: Optional[int] = 10
    offset: Optional[int] = 0
