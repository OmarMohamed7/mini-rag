from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from helpers.config import get_config, Config
from controllers import DataController
from models.enums.response_model import ResponseModel
from .schema.data import ProcessRequestSchema
from controllers.process_controller import ProcessController

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


@data_router.post("/process/{project_id}")
async def process_data(
    project_id: str,
    request: ProcessRequestSchema,
    app_settings: Config = Depends(get_config),
):

    file_id = request.file_id
    chunk_size = request.chunk_size
    overlap_size = request.overlap_size

    controller = ProcessController()
    controller.process_data(project_id=project_id)

    file_content = controller.get_file_content(file_id=request.file_id)

    file_chunks = controller.process_file_content(
        file_content=file_content,
        chunk_size=chunk_size,
        overlap_size=overlap_size,
    )

    if len(file_chunks) == 0 or file_chunks is None:
        raise HTTPException(
            status_code=400, detail=ResponseModel.FILE_NOT_PROCESSED.value
        )

    return file_chunks
