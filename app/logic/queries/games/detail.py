from dataclasses import dataclass
from uuid import UUID

from domain.entities.games import Game
from infra.repositories.developer.base import BaseDeveloperRepository
from infra.repositories.game.base import BaseGameRepository
from infra.repositories.languages.base import BaseLanguageRepository
from infra.repositories.tags.base import BaseTagRepository
from logic.exeption import NotFoundException
from logic.queries.base import BaseQuery, BaseQueryHandler


@dataclass(frozen=True)
class DetailGameQuery(BaseQuery):
    game_id: UUID


@dataclass(frozen=True)
class DetailGameQueryHandler(BaseQueryHandler[DetailGameQuery, Game]):
    game_repository: BaseGameRepository

    async def handle(self, query: DetailGameQuery) -> Game:
        game = await self.game_repository.get_by_id(id=query.game_id)

        if not game:
            raise NotFoundException('Not found Game by id')

        return game