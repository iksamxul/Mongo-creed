from fastapi import APIRouter, Depends, Query
from app.core.db import get_db
from app.repositories.universal_repository import UniversalRepository
from app.controllers.universal_controller import UniversalController

api_router = APIRouter()

def _controller(db=Depends(get_db)):
    return UniversalController(UniversalRepository(db))

@api_router.get("/{collection}")
async def list_items(collection: str, ctrl: UniversalController = Depends(_controller), limit: int = Query(20, ge=1, le=1000), offset: int = Query(0, ge=0), sort: str | None = Query(None), order: str = Query("asc", pattern="^(asc|desc)$"), q: str | None = Query(None)):
    return await ctrl.list(collection, limit, offset, sort, order, q)

@api_router.get("/{collection}/{id}")
async def get_item(collection: str, id: str, ctrl: UniversalController = Depends(_controller)):
    return await ctrl.get(collection, id)

@api_router.post("/{collection}", status_code=201)
async def create_item(collection: str, payload: dict, ctrl: UniversalController = Depends(_controller)):
    return await ctrl.create(collection, payload)

@api_router.put("/{collection}/{id}")
async def replace_item(collection: str, id: str, payload: dict, ctrl: UniversalController = Depends(_controller)):
    return await ctrl.replace(collection, id, payload)

@api_router.patch("/{collection}/{id}")
async def patch_item(collection: str, id: str, payload: dict, ctrl: UniversalController = Depends(_controller)):
    return await ctrl.patch(collection, id, payload)

@api_router.delete("/{collection}/{id}")
async def delete_item(collection: str, id: str, ctrl: UniversalController = Depends(_controller)):
    return await ctrl.delete(collection, id)
