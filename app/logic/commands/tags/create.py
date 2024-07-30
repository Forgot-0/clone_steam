from dataclasses import dataclass

from domain.entities.tags import Tag
from domain.values.base import Slug, Title
from infra.repositories.tags.base import BaseTagRepository
from logic.commands.base import BaseCommand, BaseCommandHandler



@dataclass(frozen=True)
class CreateTagCommand(BaseCommand):
    name: str
    slug: str


@dataclass(frozen=True)
class CreateTagCommandHandler(BaseCommandHandler[CreateTagCommand, Tag]):
    tag_repository: BaseTagRepository

    async def handle(self, command: CreateTagCommand) -> Tag:
        name = Title(command.name)
        slug = Slug(command.slug)

        tag = Tag(name=name, slug=slug)

        await self.tag_repository.create(tag)
        return tag