from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from app.api.routes import api_router
from app.core.db import connect, disconnect
from app.core.errors import register_exception_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect()
    yield
    await disconnect()

app = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan)
register_exception_handlers(app)
app.include_router(api_router, prefix="/api")
