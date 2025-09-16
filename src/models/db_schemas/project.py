from pydantic import Field
from models.db_schemas.base_schema_model import BaseSchemaModel


class ProjectSchema(BaseSchemaModel):

    project_id: str | None = Field(default=None, alias="_id")
    name: str | None = None
