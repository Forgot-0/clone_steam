from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable
from uuid import UUID

from domain.entities.games import Game
from infra.repositories.filters import PaginationInfra, GetGamesFiltersInfra



@dataclass
class BaseGameRepository(ABC):
    @abstractmethod
    async def create(self, game: Game) -> None:
        ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Game | None:
        ...

    @abstractmethod
    async def get_all(self, pagination: PaginationInfra) -> tuple[Iterable[Game], int]:
        ...

    @abstractmethod
    async def check_exists_by_name(self, title: str) -> bool:
        ...

    @abstractmethod
    async def get_games(self, filters: GetGamesFiltersInfra, pagination: PaginationInfra) -> tuple[Iterable[Game], int]:
        ...

    @abstractmethod
    async def delete_by_developer_id(self, id: UUID) -> None:
        ...
    
    @abstractmethod
    async def delete_by_id(self, id: UUID) -> None:
        ...


@dataclass
class MemoryGameRepository(BaseGameRepository):
    def __init__(self):
        self.db: list[Game] = list()

    async def create(self, game: Game) -> None:
        self.db.append(game)

    async def get_by_id(self, id: UUID) -> Game | None:
        for game in self.db:
            if game.id == id:
                return game
        return None

    async def get_all(self, pagination: PaginationInfra) -> tuple[Iterable[Game], int]:
        return list(filter(lambda el: not el.is_deleted, self.db[pagination.offset:pagination.limit])), len(self.db)

    async def check_exists_by_name(self, title: str) -> bool:
        for game in self.db:
            if game.title.as_generic_type() == title:
                return True
        return False

    async def get_games(self, filters: GetGamesFiltersInfra, pagination: PaginationInfra) -> tuple[Iterable[Game], int]:
        result = []
        filters_dict = {}

        if filters.developer_id is not None:
            filters_dict['developer_id'] = filters.developer_id
        
        if filters.title is not None:
            filters_dict['title'] = filters.title
        
        if filters.tags is not None:
            filters_dict['tags_id'] = set(filters.tags)
        
        if filters.languages is not None:
            filters_dict['language_id'] = set(filters.languages)

        for game in self.db:
            for key, value in filters_dict:
                attr = getattr(game, key)
                if isinstance(value, set):
                    atrr = set(el.id for el in attr)
                    if not atrr.issubset(value):
                        break
                else:
                    if attr != value:
                        break
            else:
                result.append(game)

        return result[pagination.offset:pagination.limit], len(result)