from dataclasses import dataclass
from uuid import UUID

from domain.entities.games import Game
from domain.values.base import Text, Title, Url
from infra.repositories.game.base import BaseGameRepository
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exeption import NotFoundException



@dataclass(frozen=True)
class DeleteGameCommand(BaseCommand):
    id: UUID

@dataclass(frozen=True)
class DeleteGameCommandHandler(BaseCommandHandler[DeleteGameCommand, Game]):
    game_repository: BaseGameRepository

    async def handle(self, command: DeleteGameCommand) -> Game:
        game = await self.game_repository.get_by_id(id=command.id)

        if not game:
            raise NotFoundException("NotFoundException game by id")

        await self.game_repository.delete_by_id(id=command.id)

        game.delete()
        await self.mediator.publish(game.pull_events())

        return game