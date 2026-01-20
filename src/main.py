from contextlib import asynccontextmanager

from fastapi import FastAPI

from routes import base

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Startup ready ...')
    yield
    print('Shutdown')

app = FastAPI(
    title="Mini Rag App",
    lifespan=lifespan
)

app.include_router(base.base_router)