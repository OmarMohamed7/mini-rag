from typing import Optional
from bson.objectid import ObjectId
from pydantic import BaseModel


class BaseSchema(BaseModel):

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
        json_encoders = {
            ObjectId: str,  # convert ObjectId -> str when serializing
        }
