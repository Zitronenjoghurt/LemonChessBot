from typing import Optional, Type, TypeVar
from src.entities.database_entity import DatabaseEntity
from src.scrollables.abstract_scrollable import AbstractScrollable

T = TypeVar('T', bound='AbstractQueryScrollable')

class AbstractQueryScrollable(AbstractScrollable):
    def __init__(self, page_size: int, starting_page: int = 1) -> None:
        super().__init__(page_size, starting_page)

    @classmethod
    async def create_from_find(cls: Type[T], entity_cls, page_size: int, sort_key: Optional[str] = None, descending: bool = True, **kwargs) -> T:
        entities = await entity_cls.find(
            sort_key=sort_key,
            descending=descending,
            **kwargs
        )
        return await cls.create_from_entities(entities=entities, page_size=page_size)