from fastapi import UploadFile

from src.models.enums import ResponseEnums
from .BaseView import BaseView
from src.models import ResponseMessages


class DataView(BaseView):
    def __init__(self) -> None:
        super().__init__()
        self.size_scale=1048576


    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseMessages.FILE_TYPE_NOT_SUPPORTED

        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseMessages.FILE_SIZE_EXCEEDED

        return True, ResponseMessages.FILE_VALIDATED_SUCCESS