from fastapi import APIRouter, UploadFile, File, Depends
from helpers.config import get_settings, Config
from controllers import DataController

data_router = APIRouter(
    prefix="/api/v1/data",
)


@data_router.post("/upload/{project_id}")
async def upload_data(
    project_id: str,
    file: UploadFile = File(...),
    app_settings: Config = Depends(get_settings),
):
    controller = DataController()
    return controller.upload_data(project_id, file)
