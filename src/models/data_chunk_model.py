from bson.objectid import ObjectId
from pymongo import InsertOne

from src.models.base_data_model import BaseDataModel
from src.models.db_schemas import DataChunkSchema


class DataChunk(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection = self.db_client['data_chunks']
        
    async def create_chunk(self, chunk: DataChunkSchema):
        result = await self.collection.insert_one(
            chunk.model_dump(by_alias=True, exclude_none=True)
        )
        chunk.id = result.inserted_id
        return chunk
        
    async def get_chunk(self, chunk_id: str):
        chunk = await self.collection.find_one({"_id": ObjectId(chunk_id)})
        if chunk:
            return DataChunkSchema(**chunk)
        return None
        
    async def insert_many_chunks(self, chunks: list[DataChunkSchema], batch_size: int = 100):
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            operations = [
                InsertOne(chunk.model_dump(by_alias=True, exclude_none=True))
                for chunk in batch
            ]
            
            await self.collection.bulk_write(operations)
            
        return len(chunks)
        
    async def delete_chunk_by_project_id(self, project_id: ObjectId):
        result = await self.collection.delete_many({"chunk_project_id": project_id})
        return result.deleted_count
        