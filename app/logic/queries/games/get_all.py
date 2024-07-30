from dataclasses import dataclass
from typing import Iterable

from domain.entities.games import Game
from infra.repositories.filters import PaginationInfra
from infra.repositories.game.base import BaseGameRepository
from logic.queries.base import BaseQuery, BaseQueryHandler




@dataclass(frozen=True)
class GetAllGameQuery(BaseQuery):
    pagination: PaginationInfra


@dataclass(frozen=True)
class GetAllGameQueryHandler(BaseQueryHandler[GetAllGameQuery, tuple[Iterable[Game], int]]):
    game_repository: BaseGameRepository

    async def handle(self, query: GetAllGameQuery) -> tuple[Iterable[Game], int]:
        developers, count = await self.game_repository.get_all(query.pagination)
        return developers, count