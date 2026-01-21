import os
import random
import string

from src.helpers.config import get_settings


class BaseView:
    def __init__(self) -> None:
        self.app_settings = get_settings()
        self.base_dir_path = os.path.dirname(os.path.dirname(__file__))
        self.files_dir_path = os.path.join(
            self.base_dir_path,
            "assets/files"
        )

    def generate_random_string(self, length: int=12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

