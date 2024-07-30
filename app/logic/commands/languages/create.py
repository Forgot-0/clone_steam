from dataclasses import dataclass

from domain.entities.languages import Language
from domain.values.base import Slug, Title
from infra.repositories.languages.base import BaseLanguageRepository
from logic.commands.base import BaseCommand, BaseCommandHandler


@dataclass(frozen=True)
class CreateLanguageCommand(BaseCommand):
    lang: str
    slug: str
    interface: bool
    full_audio: bool
    subtitles: bool


@dataclass(frozen=True)
class CreateLanguageCommandHandler(BaseCommandHandler[CreateLanguageCommand, Language]):
    language_repository: BaseLanguageRepository

    async def handle(self, command: CreateLanguageCommand) -> Language:
        
        language = Language(
            lang=Title(command.lang),
            slug=Slug(command.slug),
            interface=command.interface,
            full_audio=command.full_audio,
            subtitles=command.subtitles
        )
        await self.language_repository.create(language=language)

        return language

