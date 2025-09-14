from .base_controller import BaseController
from fastapi import UploadFile, File, HTTPException


class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576

    def validate_file(self, file: UploadFile) -> bool:
        if file.content_type not in self.app_config.FILE_ALLOWED_EXTENSTIONS:
            raise HTTPException(status_code=400, detail="File type not allowed")

        if file.size > self.app_config.FILE_MAX_SIZE * self.size_scale:
            raise HTTPException(status_code=400, detail="File size is too large")

        if file.size == 0:
            raise HTTPException(status_code=400, detail="File is empty")

        return True

    def upload_data(self, project_id: str, file: UploadFile = File(...)) -> dict:
        if not self.validate_file(file):
            raise HTTPException(status_code=400, detail="File is not valid")

        return {"message": "Data", "project_id": project_id, "file": file.filename}
