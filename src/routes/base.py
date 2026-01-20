from fastapi import APIRouter, Depends

from src.helpers.config import Settings, get_settings

base_router = APIRouter(
    prefix='/api/v1',
    tags= ['api_v1']
)

@base_router.get('/')
def welcome(app_settings: Settings = Depends(get_settings)):
    settings_dict = app_settings.model_dump()
    app_name = settings_dict.get('APP_NAME')
    app_version = settings_dict.get('APP_VERSION')

    return {
        'app_name': app_name,
        'app_version': app_version,
    }