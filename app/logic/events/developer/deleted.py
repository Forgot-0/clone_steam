from dataclasses import dataclass

from domain.events.developers.developer_deleted import DeveloperDeleted
from infra.repositories.game.base import BaseGameRepository
from logic.events.base import BaseEventHandler



@dataclass(frozen=True)
class DeletedDeveloperEventHandler(BaseEventHandler[DeveloperDeleted, None]):
    game_repository: BaseGameRepository

    async def handle(self, event: DeveloperDeleted) -> None:
        await self.game_repository.delete_by_developer_id(id=event.id)
