from dataclasses import dataclass

from domain.events.developers.deleted import DeletedDeveloperEvent
from infra.repositories.game.base import BaseGameRepository
from logic.events.base import BaseEventHandler



@dataclass(frozen=True)
class DeletedDeveloperEventHandler(BaseEventHandler[DeletedDeveloperEvent, None]):
    game_repository: BaseGameRepository

    async def handle(self, event: DeletedDeveloperEvent) -> None:
        await self.game_repository.delete_by_developer_id(id=event.id)
