from src.helpers.config import get_settings


class BaseView:
    def __init__(self) -> None:
        self.app_settings = get_settings()