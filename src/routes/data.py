import logging

from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
import aiofiles

from src.helpers.config import Settings, get_settings
from src.views import DataView, ProjectView
from src.models import ResponseMessages

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix='/api/v1/data',
    tags= ['api_v1', 'data']
)


@data_router.post('/upload/{project_id}', status_code=status.HTTP_200_OK)
async def upload(project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    
    data_view = DataView()
    is_valid, message = data_view.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content= {
                "message": message
            }
        )

    file_location, file_id = data_view.generate_unique_filepath(
        orig_file_name=file.filename,
        project_id=project_id
    )
    chunk_size = app_settings.FILE_DEFAULT_CHUNK_SIZE

    async def save_file():
        async with aiofiles.open(file_location, 'wb') as out_file:
            while True:
                chunk = await file.read(chunk_size)
                if not chunk:
                    break
                await out_file.write(chunk)
        await file.close()

    try:
        await save_file()
    except Exception as e:
        logger.error(f"File upload failed: {e}")
        return JSONResponse(
            content={
                "message": ResponseMessages.FILE_UPLOAD_FAILED
            }
        )

    return JSONResponse(
            content={
                "message": ResponseMessages.FILE_UPLOAD_SUCCESS,
                'file_id': file_id
            }
        )