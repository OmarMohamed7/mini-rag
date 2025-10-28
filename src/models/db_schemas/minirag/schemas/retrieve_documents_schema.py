from pydantic import Field


class RetrieveDocumentsSchema:
    text: str = Field(..., min_length=1)
    score: float
