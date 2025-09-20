from pydantic import Field
from pymongo import IndexModel
from models.db_schemas.base_schema import BaseSchema


class ProjectSchema(BaseSchema):
    project_id: str | None = Field(default=None, alias="_id")
    name: str | None = None

    @classmethod
    def get_indexes(cls):
        return [
            IndexModel([("project_id", 1)], unique=True, name="project_id_index"),
        ]
