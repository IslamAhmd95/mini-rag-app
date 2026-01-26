from typing import Any

from src.helpers.config import get_settings


class BaseDataModel:
    def __init__(self, db_client: Any):
        self.db_client = db_client
        self.app_settings = get_settings()