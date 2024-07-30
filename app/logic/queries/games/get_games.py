from dataclasses import dataclass
from typing import Iterable

from domain.entities.games import Game
from infra.repositories.filters import GetGamesFiltersInfra, PaginationInfra
from infra.repositories.game.base import BaseGameRepository
from logic.queries.base import BaseQuery, BaseQueryHandler


@dataclass(frozen=True)
class GetGamesFilterQuery(BaseQuery):
    pagination: PaginationInfra
    filters: GetGamesFiltersInfra


@dataclass(frozen=True)
class GetGamesFilterQueryHandler(BaseQueryHandler[GetGamesFilterQuery, tuple[Iterable[Game], int]]):
    game_repository: BaseGameRepository

    async def handle(self, query: GetGamesFilterQuery) -> tuple[Iterable[Game], int]:
        result, count = await self.game_repository.get_games(filters=query.filters, pagination=query.pagination)
        return result, count 