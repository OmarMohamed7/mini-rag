from bson import ObjectId
from models.base_data_model import BaseDataModel
from models.db_schemas.asset_schema import AssetSchema
from models.enums.database_enum import DatabaseEnum


class AssetModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection = self.db_client[DatabaseEnum.ASSET.value]

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DatabaseEnum.ASSET.value not in all_collections:
            self.collection = self.db_client[DatabaseEnum.ASSET.value]
            await self.collection.create_indexes(AssetSchema.get_indexes())

    async def create_asset(self, asset: AssetSchema):
        res = await self.collection.insert_one(
            asset.model_dump(by_alias=True, exclude_none=True)
        )
        asset.id = res.inserted_id
        return asset

    async def get_asset(self, asset_id: str):
        res = await self.collection.find_one({"_id": asset_id})
        if res is None:
            return None
        return AssetSchema(**res)

    async def get_project_assets(
        self, project_id: str, asset_type: str = "File", page: int = 1, limit: int = 10
    ):

        # count total number of documents
        total_documents = await self.collection.count_documents(
            {"asset_project_id": ObjectId(project_id), "asset_type": asset_type}
        )

        # calculate total number of pages
        total_pages = total_documents // limit
        if total_documents % limit > 0:
            total_pages += 1

        res = (
            await self.collection.find(
                {"asset_project_id": ObjectId(project_id), "asset_type": asset_type}
            )
            .skip((page - 1) * limit)
            .limit(limit)
            .to_list(length=None)
        )

        return [AssetSchema(**asset) for asset in res], total_pages

    async def get_asset_by_type(self, asset_type: str):
        res = await self.collection.find({"asset_type": asset_type}).to_list(
            length=None
        )
        if res is None:
            return None
        return [AssetSchema(**asset) for asset in res]

    async def get_all_assets(self):
        return await self.collection.find().to_list(length=None)

    async def delete_asset(self, asset_id: str):
        return await self.collection.delete_one({"_id": asset_id})
