from controllers.project_controller import ProjectController
from .base_controller import BaseController
from fastapi import UploadFile, File, HTTPException
from models import ResponseModel
import os
import aiofiles
import re


class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576

    async def validate_file(self, file: UploadFile) -> bool:
        if file.content_type not in self.app_config.FILE_ALLOWED_EXTENSTIONS:
            raise HTTPException(
                status_code=400, detail=ResponseModel.FILE_TYPE_NOT_ALLOWED.value
            )

        if file.size > self.app_config.FILE_MAX_SIZE * self.size_scale:
            raise HTTPException(
                status_code=400, detail=ResponseModel.FILE_SIZE_TOO_LARGE.value
            )

        if file.size == 0:
            raise HTTPException(status_code=400, detail=ResponseModel.FILE_EMPTY.value)

        return True

    def generate_file_name(self, original_name: str, project_id: str) -> str:
        random_string = self.generate_random_string()

        project_path = ProjectController().get_project(project_id)

        clean_file_name = self.get_clean_file_name(original_name)

        file_path = os.path.join(project_path, random_string + "_" + clean_file_name)

        while os.path.exists(file_path):
            random_string = self.generate_random_string()
            file_path = os.path.join(
                project_path, random_string + "_" + clean_file_name
            )

        return file_path

    async def upload_data(self, project_id: str, file: UploadFile = File(...)) -> dict:

        if not await self.validate_file(file):
            raise HTTPException(
                status_code=400, detail=ResponseModel.FILE_NOT_VALIDATED.value
            )

        file_path = self.generate_file_name(file.filename, project_id)

        try:
            async with aiofiles.open(file_path, "wb") as f:
                # Optimized to not read the entire file into memory
                # This is a more efficient way to read the file
                # It reads the file in chunks of the size of the file chunk default size
                while chunk := await file.read(self.app_config.FILE_CHUNK_DEFAULT_SIZE):
                    await f.write(chunk)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=str(ResponseModel.FILE_NOT_UPLOADED.value)
            )

        return {
            "message": ResponseModel.FILE_UPLOADED.value,
            "project_id": project_id,
            "file": file_path.split("/")[-1],
            "project_path": file_path,
        }

    def get_clean_file_name(self, file_name: str) -> str:
        clean_file_name = re.sub(r"[^\w.]", "", file_name)
        return clean_file_name.replace(" ", "_")
