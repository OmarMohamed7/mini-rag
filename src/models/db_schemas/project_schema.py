from typing import Optional
from bson.objectid import ObjectId
from pydantic import Field
from pymongo import IndexModel
from models.db_schemas.base_schema import BaseSchema


class ProjectSchema(BaseSchema):
    id: Optional[ObjectId] = Field(None, alias="_id")
    project_id: str = Field(..., min_length=1)

    @classmethod
    def get_indexes(cls):
        return [
            IndexModel([("project_id", 1)], unique=True, name="project_id_index"),
        ]
