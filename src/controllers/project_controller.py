import json
from fastapi import HTTPException
from models import ResponseModel
from .base_controller import BaseController
import os


class ProjectController(BaseController):

    def __init__(self):
        super().__init__()

    def create_project(self, project_name: str) -> dict:
        project_path = os.path.join(self.files_dir, project_name)
        os.makedirs(project_path, exist_ok=True)

        return {
            "message": ResponseModel.PROJECT_CREATED.value,
            "project_name": project_name,
        }

    def get_project(self, project_id: str) -> dict:

        project_path = os.path.join(self.files_dir, project_id)

        if not os.path.exists(project_path):
            self.create_project(project_id)

        return project_path
