from typing import Optional
from pydantic import BaseModel


class ProcessRequestSchema(BaseModel):
    file_id: str
    chunk_size: Optional[int] = 100
    overlap_size: Optional[int] = 20
    de_reset: Optional[int] = 0
