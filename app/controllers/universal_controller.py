from __future__ import annotations
from typing import Any, Dict, Optional
import json
from app.core.errors import AppError
from app.repositories.universal_repository import UniversalRepository
from app.utils.bson import to_object_id, serialize_doc

class UniversalController:
    def __init__(self, repo: UniversalRepository) -> None:
        self.repo = repo

    def _validate_collection(self, name: str) -> str:
        if not name or not all(c.isalnum() or c in {"_", ".", "-"} for c in name):
            raise AppError(400, "Invalid collection")
        return name

    def _parse_filter(self, q: Optional[str]) -> Dict[str, Any]:
        if not q:
            return {}
        try:
            data = json.loads(q)
            if not isinstance(data, dict):
                raise AppError(400, "Query filter must be an object")
            if "_id" in data and isinstance(data["_id"], str):
                try:
                    data["_id"] = to_object_id(data["_id"])
                except ValueError:
                    raise AppError(400, "Invalid ObjectId in filter")
            return data
        except json.JSONDecodeError:
            raise AppError(400, "Invalid JSON in filter")

    async def list(self, collection: str, limit: int, offset: int, sort: Optional[str], order: str, q: Optional[str]):
        name = self._validate_collection(collection)
        filt = self._parse_filter(q)
        sort_tuple = None
        if sort:
            sort_tuple = (sort, 1 if order == "asc" else -1)
        items, total = await self.repo.list(name, filt, limit, offset, sort_tuple)
        return {
            "items": [serialize_doc(d) for d in items],
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    async def get(self, collection: str, id: str):
        name = self._validate_collection(collection)
        try:
            oid = to_object_id(id)
        except ValueError:
            raise AppError(400, "Invalid id")
        doc = await self.repo.get(name, oid)
        if not doc:
            raise AppError(404, "Not found")
        return serialize_doc(doc)

    async def create(self, collection: str, payload: Dict[str, Any]):
        name = self._validate_collection(collection)
        if not isinstance(payload, dict):
            raise AppError(400, "Body must be an object")
        payload.pop("id", None)
        payload.pop("_id", None)
        doc = await self.repo.create(name, payload)
        return serialize_doc(doc)

    async def replace(self, collection: str, id: str, payload: Dict[str, Any]):
        name = self._validate_collection(collection)
        if not isinstance(payload, dict):
            raise AppError(400, "Body must be an object")
        try:
            oid = to_object_id(id)
        except ValueError:
            raise AppError(400, "Invalid id")
        payload.pop("id", None)
        payload.pop("_id", None)
        doc = await self.repo.replace(name, oid, payload)
        if not doc:
            raise AppError(404, "Not found")
        return serialize_doc(doc)

    async def patch(self, collection: str, id: str, payload: Dict[str, Any]):
        name = self._validate_collection(collection)
        if not isinstance(payload, dict):
            raise AppError(400, "Body must be an object")
        try:
            oid = to_object_id(id)
        except ValueError:
            raise AppError(400, "Invalid id")
        payload.pop("id", None)
        payload.pop("_id", None)
        doc = await self.repo.update_fields(name, oid, payload)
        if not doc:
            raise AppError(404, "Not found")
        return serialize_doc(doc)

    async def delete(self, collection: str, id: str):
        name = self._validate_collection(collection)
        try:
            oid = to_object_id(id)
        except ValueError:
            raise AppError(400, "Invalid id")
        ok = await self.repo.delete(name, oid)
        if not ok:
            raise AppError(404, "Not found")
        return {"deleted": True}
