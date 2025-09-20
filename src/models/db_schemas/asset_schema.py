from datetime import datetime
from typing import Optional
from bson.objectid import ObjectId
from pydantic import Field
from pymongo import IndexModel

from models.db_schemas.base_schema import BaseSchema


class AssetSchema(BaseSchema):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    asset_project_id: str
    asset_name: str
    asset_type: str
    asset_created_at: datetime = Field(default=datetime.now())
    asset_size: int = Field(default=None, gt=0)

    @classmethod
    def get_indexes(cls):
        return [
            IndexModel(
                [("asset_project_id", 1)], unique=False, name="asset_project_id_index"
            ),
            IndexModel(
                [("asset_name", 1), ("asset_project_id", 1)],
                unique=True,
                name="asset_name_project_id_index",
            ),
        ]
