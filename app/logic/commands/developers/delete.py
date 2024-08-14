from dataclasses import dataclass

from domain.entities.developers import Developer
from infra.repositories.developer.base import BaseDeveloperRepository
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exeption import NotFoundException



@dataclass(frozen=True)
class DeleteDeveloperCommand(BaseCommand):
    id: str


@dataclass(frozen=True)
class DeleteDeveloperCommandHandler(BaseCommandHandler[DeleteDeveloperCommand, Developer]):
    developer_repository: BaseDeveloperRepository

    async def handle(self, command: DeleteDeveloperCommand) -> None:
        developer = await self.developer_repository.get_by_id(id=command.id)

        if not developer:
            raise NotFoundException('developer id')

        developer.delete()

        await self.mediator.publish(developer.pull_events())

        await self.developer_repository.update(developer=developer)
