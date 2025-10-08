from helpers.config import get_config
import os
import string
import random


class BaseController:
    def __init__(self):
        self.app_config = get_config()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.files_dir = os.path.join(self.base_dir, "assets", "files")
        self.database_dir = os.path.join(self.base_dir, "assets", "database")

    def generate_random_string(self, length: int = 10) -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    def get_database_path(self, database_name: str) -> str:
        database_path = os.path.join(self.database_dir, database_name)
        if not os.path.exists(database_path):
            os.makedirs(database_path, exist_ok=True)
        return database_path
