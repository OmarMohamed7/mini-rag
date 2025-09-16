from typing import Optional
from bson.objectid import ObjectId
from helpers.config import get_config


class BaseDataModel:
    def __init__(self, db_client: object):
        self.db_client = db_client
        self.app_config = get_config()
