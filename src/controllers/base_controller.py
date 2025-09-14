from helpers.config import get_config


class BaseController:
    def __init__(self):
        self.app_config = get_config()
