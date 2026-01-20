import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import APIRouter


base_router = APIRouter(
    prefix='/api/v1',
    tags= ['api_v1']
)

@base_router.get('/')
def welcome():
    app_name = os.getenv('APP_NAME')
    app_version = os.getenv('APP_VERSION')

    return {
        'app name': app_name,
        'app version': app_version,
    }