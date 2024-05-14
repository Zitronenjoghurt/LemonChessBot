from typing import ClassVar, Optional, Type, TypeVar
from pydantic import BaseModel
from src.db import Database, Collection

DB = Database.get_instance()

T = TypeVar('T', bound='DatabaseEntity')
class DatabaseEntity(BaseModel):
    COLLECTION: ClassVar[Collection] = Collection.NONE
    _id: str

    @classmethod
    async def find_one(cls: Type[T], **kwargs) -> Optional[T]:
        result = await DB.find_one(cls.COLLECTION, **kwargs)
        if result:
            return cls.model_validate(result)
        return None
    
    @classmethod
    async def find(cls: Type[T], **kwargs) -> list[T]:
        results = await DB.find(cls.COLLECTION, **kwargs)
        return [cls.model_validate(result) for result in results]
    
    async def save(self):
        document = self.model_dump()
        await DB.save(self.COLLECTION, document)
    
    @classmethod
    async def load(cls: Type[T], **kwargs) -> T:
        instance = await cls.find_one(**kwargs)
        if instance:
            return instance
        return cls.model_validate(kwargs)