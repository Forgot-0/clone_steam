from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable
from uuid import UUID

from domain.entities.games import Tag
from infra.repositories.filters import PaginationInfra


@dataclass
class BaseTagRepository(ABC):

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Tag:
        ...

    @abstractmethod 
    async def create(self, tag: Tag) -> None:
        ...

    @abstractmethod
    async def get_all(self, pagination: PaginationInfra) -> tuple[Iterable[Tag], int]:
        ...


@dataclass
class MemoryTagRepository(BaseTagRepository):
    def __init__(self):
        self.db: list[Tag] = list()

    async def get_by_id(self, id: UUID) -> Tag | None:
        for tag in self.db:
            if tag.id == id:
                return tag
        return None

    async def create(self, tag: Tag) -> None:
        self.db.append(tag)

    async def get_all(self, pagination: PaginationInfra) -> tuple[Iterable[Tag], int]:
        return self.db[pagination.offset:pagination.limit], len(self.db)