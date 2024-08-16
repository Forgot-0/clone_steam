from dataclasses import dataclass

from domain.entities.developers import Developer
from domain.values.base import Email, Slug, Text
from infra.repositories.developer.base import BaseDeveloperRepository
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exeption import EmailAlreadyExistsException, IsDeleted, NameAlreadyExistsException



@dataclass(frozen=True)
class CreateDeveloperCommand(BaseCommand):
    name: str
    slug: str
    email: str


@dataclass(frozen=True)
class CreateDeveloperCommandHandler(BaseCommandHandler[CreateDeveloperCommand, Developer]):
    developer_repository: BaseDeveloperRepository

    async def handle(self, command: CreateDeveloperCommand) -> Developer:
        if await self.developer_repository.check_exists_by_name(command.name):
            raise NameAlreadyExistsException(command.name)

        developer = await self.developer_repository.get_by_email(command.email)
        if developer:
            if developer.is_deleted:
                raise IsDeleted(developer.email)
            raise EmailAlreadyExistsException(command.email)

        name = Text(command.name)
        slug = Slug(command.slug)
        email = Email(command.email)

        developer = Developer.create_developer(name=name, slug=slug, email=email)
        await self.developer_repository.create(developer)

        await self.mediator.publish(developer.pull_events())
        return developer