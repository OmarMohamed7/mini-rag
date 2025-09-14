from fastapi import APIRouter, UploadFile, File, Depends
from helpers.config import get_config, Config
from controllers import DataController

data_router = APIRouter(
    prefix="/api/v1/data",
)


@data_router.post("/upload/{project_id}")
async def upload_data(
    project_id: str,
    file: UploadFile = File(...),
    app_settings: Config = Depends(get_config),
):
    controller = DataController()
    return await controller.upload_data(project_id, file)
