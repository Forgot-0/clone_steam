from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable
from uuid import UUID

from domain.entities.games import Language
from infra.repositories.filters import PaginationInfra


@dataclass
class BaseLanguageRepository(ABC):

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Language | None:
        ...

    @abstractmethod 
    async def create(self, language: Language) -> None:
        ...

    @abstractmethod
    async def get_all(self, pagination: PaginationInfra) -> tuple[Iterable[Language], int]:
        ...


@dataclass
class MemoryLanguageRepository(BaseLanguageRepository):
    def __init__(self):
        self.db: list[Language] = list()

    async def get_by_id(self, id: UUID) -> Language | None:
        for language in self.db:
            if language.id == id:
                return language
        return None

    async def create(self, language: Language) -> None:
        self.db.append(language)

    async def get_all(self, pagination: PaginationInfra) -> tuple[Iterable[Language], int]:
        return self.db[pagination.offset:pagination.limit], len(self.db)