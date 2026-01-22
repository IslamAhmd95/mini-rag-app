import logging

from fastapi import APIRouter, Depends, UploadFile, status
import aiofiles

from src.helpers.config import Settings, get_settings
from src.helpers.utils import json_response
from src.views import DataView, ProcessView
from src.models import ResponseMessages
from src.schemas import ProcessRequest


logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix='/api/v1/data',
    tags= ['api_v1', 'data']
)


@data_router.post('/upload/{project_id}', status_code=status.HTTP_200_OK)
async def upload_file(project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    
    data_view = DataView(project_id=project_id)
    is_valid, message = data_view.validate_uploaded_file(file=file)

    if not is_valid:
        return json_response(message=message, status=400)

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

    try:
        await save_file()
    except Exception as e:
        logger.error(f"File upload failed: {e}")
        return json_response(message=ResponseMessages.FILE_UPLOAD_FAILED, status=500)

    return json_response(message=ResponseMessages.FILE_UPLOAD_SUCCESS, data={'file_id': file_id})


@data_router.post('/process/{project_id}')
async def process_file(project_id: str, process_request: ProcessRequest):
    file_id, chunk_size, overlap_size = process_request.file_id, process_request.chunk_size, process_request.overlap_size

    process_view = ProcessView(project_id=project_id)
    file_content = process_view.get_file_content(file_id=file_id)
    file_chunks = process_view.process_file_content(
        file_content=file_content,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )

    if file_chunks is None or len(file_chunks) == 0:
        return json_response(message=ResponseMessages.FILE_PROCESS_FAILED, status=400)

    return json_response(
        message=ResponseMessages.FILE_PROCESS_SUCCESS,
        data={'file_chunks': [
            chunk.to_dict() if hasattr(chunk, 'to_dict') else dict(chunk)
        for chunk in file_chunks
        ]}
    )

