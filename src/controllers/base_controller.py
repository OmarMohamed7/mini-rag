from helpers.config import get_config
import os
import string
import random


class BaseController:
    def __init__(self):
        self.app_config = get_config()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.files_dir = os.path.join(self.base_dir, "assets", "files")

    def generate_random_string(self, length: int = 10) -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))
