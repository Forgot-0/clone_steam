from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable

from domain.entities.base import AggregateRoot
from domain.entities.developers import Developer
from domain.entities.languages import Language
from domain.entities.tags import Tag
from domain.exception.base import AlreadyDeletedException
from domain.values.base import Text, Title, Url





@dataclass(eq=False)
class Game(AggregateRoot):
    title: Title
    description: Text

    release_date: datetime

    developer: Developer

    medias: list[Url] = field(default_factory=list, kw_only=True)
    languages: list[Language] = field(default_factory=list, kw_only=True)
    tags: list[Tag] = field(default_factory=list, kw_only=True)

    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True
    )
    is_deleted: bool = field(default=False, kw_only=True)

    @classmethod
    def create_game(
            cls, 
            title: Title,
            description: Text,
            developer: Developer,
            release_date: datetime
        ) -> 'Game':
        return cls(
            title=title,
            description=description,
            developer=developer,
            release_date=release_date
        )

    def add_tags(self, tags: Iterable[Tag]) -> None:
        self.tags.extend(tags)

    def add_medias(self, medias: Iterable[Url]) -> None:
        self.medias.extend(medias)

    def add_languages(self, languages: Iterable[Language]) -> None:    
        self.languages.extend(languages)

    def delete(self) -> None:
        if self.is_deleted:
            raise AlreadyDeletedException()

        self.is_deleted = True