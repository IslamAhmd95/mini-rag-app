import logging

from fastapi import APIRouter, Depends, UploadFile, status, Request
import aiofiles

from src.helpers.config import Settings, get_settings
from src.helpers.utils import json_response
from src.models.data_chunk_model import DataChunk
from src.models.db_schemas.data_chunk_schema import DataChunkSchema
from src.models.project_model import ProjectModel
from src.views import DataView, ProcessView
from src.models import ResponseMessages
from src.schemas import ProcessRequest


logger = logging.getLogger('uvicorn.error')  # uvicorn.error is the name of this logger and the scope is uvicorn server logs which can be used on several files

data_router = APIRouter(
    prefix='/api/v1/data',
    tags= ['api_v1', 'data']
)


@data_router.post('/upload/{project_id}', status_code=status.HTTP_200_OK)
async def upload_file(request: Request, project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    
    project_model = ProjectModel(
        db_client=request.app.state.db_client
    )
    
    await project_model.get_project_or_create_one(project_id=project_id)
    
    data_view = DataView(project_id=project_id)
    is_valid, message = data_view.validate_uploaded_file(file=file)

    if not is_valid:
        return json_response(message=message, status=400)

    if file.filename is None:
        return json_response(message="Filename is required", status=400)

    file_location, file_id = data_view.generate_unique_filepath(
        project_id=project_id,
        orig_file_name=file.filename
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
async def process_file(request: Request, project_id: str, process_request: ProcessRequest):
    
    file_id, chunk_size, overlap_size, do_reset = process_request.file_id, process_request.chunk_size, process_request.overlap_size, process_request.do_reset

    process_view = ProcessView(project_id=project_id)
    file_content = process_view.get_file_content(file_id=file_id)
    
    if file_content is None:
        return json_response(message=ResponseMessages.FILE_NOT_FOUND, status=400)
    
    file_chunks = process_view.process_file_content(
        file_content=file_content,
        chunk_size=chunk_size or 100,
        overlap_size=overlap_size or 20
    )


    if file_chunks is None or len(file_chunks) == 0:
        return json_response(message=ResponseMessages.CHUNKS_NOT_FOUND, status=400)
        
    
    project_model = ProjectModel(
        db_client=request.app.state.db_client
    )
    
    project = await project_model.get_project_or_create_one(project_id=project_id)
    
    if project.id is None:
        return json_response(message=ResponseMessages.PROJECT_NOT_FOUND, status=400)
    
    chunk_model = DataChunk(
        db_client=request.app.state.db_client
    )
    
    chunks_records = [
        DataChunkSchema(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order=i+1,
            chunk_project_id=project.id,
        )
        for i, chunk in enumerate(file_chunks)
    ]
    
    if do_reset == 1:
        await chunk_model.delete_chunk_by_project_id(
            project_id=project.id
        )
    
    no_records = await chunk_model.insert_many_chunks(chunks_records)

    return json_response(
        message=ResponseMessages.FILE_PROCESS_SUCCESS,
        data={'number_of_records': no_records}
    )


