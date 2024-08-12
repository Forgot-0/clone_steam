from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.entities.games import Game
from domain.values.base import Text, Title, Url
from infra.repositories.developer.base import BaseDeveloperRepository
from infra.repositories.game.base import BaseGameRepository
from infra.repositories.languages.base import BaseLanguageRepository
from infra.repositories.tags.base import BaseTagRepository
from logic.commands.base import BaseCommand, BaseCommandHandler



@dataclass(frozen=True)
class CreateGameCommand(BaseCommand):
    title: str
    description: str

    release_date: datetime

    developer_id: UUID
    medias: list[str]
    tags: list[UUID]
    languages: list[UUID]


@dataclass(frozen=True)
class CreateGameCommandHandler(BaseCommandHandler[CreateGameCommand, Game]):
    game_repository: BaseGameRepository
    developer_repository: BaseDeveloperRepository
    tag_repository: BaseTagRepository
    language_repository: BaseLanguageRepository

    async def handle(self, command: CreateGameCommand) -> Game:
        developer = await self.developer_repository.get_by_id(id=command.developer_id)

        game = Game.create_game(
            title=Title(command.title),
            description=Text(command.description),
            developer=developer,
            release_date=command.release_date
        )

        game.medias = [Url(media) for media in command.medias]
        game.languages = [await self.language_repository.get_by_id(language) for language in command.languages]
        game.tags = [await self.tag_repository.get_by_id(tag_id) for tag_id in command.tags]

        await self.game_repository.create(game)

        return game