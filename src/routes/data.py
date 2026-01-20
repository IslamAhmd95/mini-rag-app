from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse

from src.helpers.config import Settings, get_settings
from src.views.DataView import DataView


data_router = APIRouter(
    prefix='/api/v1/data',
    tags= ['api_v1', 'data']
)


@data_router.post('/upload/{project_id}', status_code=status.HTTP_200_OK)
def upload(project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    
    data_view = DataView()
    is_valid, message = data_view.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content= {
                "message": message
            }
        )

    return JSONResponse(
            content={
                "message": message
            }
        )