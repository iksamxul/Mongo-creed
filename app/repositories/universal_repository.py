from __future__ import annotations
from typing import Any, Dict, Optional, Tuple
from datetime import datetime
from bson import ObjectId
from pymongo import ReturnDocument
from motor.motor_asyncio import AsyncIOMotorDatabase

class UniversalRepository:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db = db

    def _coll(self, name: str):
        return self.db[name]

    async def list(self, name: str, filt: Dict[str, Any], limit: int, offset: int, sort: Optional[Tuple[str, int]]):
        cursor = self._coll(name).find(filt, skip=offset, limit=limit)
        if sort:
            cursor = cursor.sort([sort])
        items = await cursor.to_list(length=limit)
        total = await self._coll(name).count_documents(filt)
        return items, total

    async def get(self, name: str, oid: ObjectId):
        return await self._coll(name).find_one({"_id": oid})

    async def create(self, name: str, data: Dict[str, Any]):
        now = datetime.utcnow()
        data = {**data, "_id": ObjectId(), "created_at": now, "updated_at": now}
        await self._coll(name).insert_one(data)
        return data

    async def replace(self, name: str, oid: ObjectId, data: Dict[str, Any]):
        now = datetime.utcnow()
        data = {**data, "_id": oid, "updated_at": now}
        res = await self._coll(name).replace_one({"_id": oid}, data, upsert=False)
        if res.matched_count == 0:
            return None
        return await self.get(name, oid)

    async def update_fields(self, name: str, oid: ObjectId, fields: Dict[str, Any]):
        fields.pop("_id", None)
        res = await self._coll(name).find_one_and_update(
            {"_id": oid},
            {"$set": {**fields, "updated_at": datetime.utcnow()}},
            return_document=ReturnDocument.AFTER,
        )
        return res

    async def delete(self, name: str, oid: ObjectId) -> bool:
        res = await self._coll(name).delete_one({"_id": oid})
        return res.deleted_count > 0
