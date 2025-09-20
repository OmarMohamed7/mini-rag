from models.base_data_model import BaseDataModel
from models.db_schemas.project import ProjectSchema
from models.enums.database_enum import DatabaseEnum


class ProjectModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection = self.db_client[DatabaseEnum.COLLECTION_PROJECT.value]

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DatabaseEnum.COLLECTION_PROJECT.value not in all_collections:
            self.collection = self.db_client[DatabaseEnum.COLLECTION_PROJECT.value]
            await self.collection.create_indexes(ProjectSchema.get_indexes())

    async def create_project(self, project: ProjectSchema):
        res = await self.collection.insert_one(
            project.model_dump(by_alias=True, exclude_none=True)
        )
        project.project_id = str(res.inserted_id)
        return project

    async def get_or_create_project(self, project_id: str):
        res = await self.collection.find_one({"_id": project_id})
        if res is None:
            # create project
            project = ProjectSchema()
            project.project_id = project_id
            project_result = await self.create_project(project)
            return project_result
        else:
            # convert from dict to model
            return ProjectSchema(**res)

    async def get_all_projects(self, page: int = 1, limit: int = 10):
        res = (
            await self.collection.find()
            .skip((page - 1) * limit)
            .limit(limit)
            .to_list(length=None)
        )

        return [ProjectSchema(**project) for project in res]
