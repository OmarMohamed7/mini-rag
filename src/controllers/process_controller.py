import os

from langchain_core.documents import Document
from .base_controller import BaseController
from routes.schema.data import ProcessRequestSchema
from controllers.project_controller import ProjectController
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from models import AllowedFileExtensions


class ProcessController(BaseController):

    def __init__(self, project_id: str):
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project(project_id)

    def get_file_extension(self, file_id: str):
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self, file_name: str):
        file_extension = self.get_file_extension(file_name)

        file_path = os.path.join(self.project_path, file_name)

        if not os.path.exists(file_path):
            raise ValueError(f"File not found: {file_path}")

        if file_extension == AllowedFileExtensions.PDF.value:
            return PyMuPDFLoader(file_path)

        elif file_extension == AllowedFileExtensions.TXT.value:
            return TextLoader(file_path, encoding="utf-8")

        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")

    def get_file_content(self, file_name: str):
        loader = self.get_file_loader(file_name)
        if loader is None:
            return None
        return loader.load()

    def process_file_content(
        self,
        file_content: list[Document],
        chunk_size: int = 100,
        overlap_size: int = 20,
    ):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len,
        )

        file_content_texts = [rec.page_content for rec in file_content]
        file_content_metadata = [rec.metadata for rec in file_content]

        # Every Chunck will have its metadata
        file_content_chunks = text_splitter.create_documents(
            file_content_texts, file_content_metadata
        )

        return file_content_chunks
