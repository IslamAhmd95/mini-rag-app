from contextlib import asynccontextmanager

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from src.routes import base, data
from src.helpers.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Startup ready ...')
    app_settings = get_settings()
    app.state.mongo_conn = AsyncIOMotorClient(app_settings.MONGODB_URL)
    app.state.db_client = app.state.mongo_conn[app_settings.MONGODB_DATABASE]
    
    yield
    
    app.state.mongo_conn.close()
    print('Shutdown')


app = FastAPI(
    title="Mini Rag App",
    lifespan=lifespan
)

app.include_router(base.base_router)
app.include_router(data.data_router)