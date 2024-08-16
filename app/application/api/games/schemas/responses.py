from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from application.api.developers.schemas.responses import DeveloperDetailSchema
from application.api.languages.schemas.responses import LanguageDetailSchema
from application.api.schemas import BaseQueryResponseSchema
from application.api.tags.schemas.responses import TagDetailSchema
from domain.entities.games import Game





class GameDetailSchema(BaseModel):
    id: UUID
    title: str
    description: str

    release_date: datetime

    developer: DeveloperDetailSchema
    medias: list[str]
    languages: list[LanguageDetailSchema]
    tags: list[TagDetailSchema]

    created_at: datetime

    @classmethod
    def from_entity(cls, game: Game) -> 'GameDetailSchema':
        return cls(
            id=game.id,
            title=game.title.as_generic_type(),
            description=game.description.as_generic_type(),
            release_date=game.release_date,
            developer=DeveloperDetailSchema.from_entity(game.developer),
            medias=[media.as_generic_type() for media in game.medias],
            languages=[LanguageDetailSchema.from_entity(lang) for lang in game.languages],
            tags=[TagDetailSchema.from_entity(tag) for tag in game.tags],
            created_at=game.created_at
        )


class GameDetailForAllSchema(BaseModel):
    id: UUID
    title: str
    description: str

    release_date: datetime

    developer: DeveloperDetailSchema
    tags: list[TagDetailSchema]

    created_at: datetime

    @classmethod
    def from_entity(cls, game: Game) -> 'GameDetailForAllSchema':
        return cls(
            id=game.id,
            title=game.title.as_generic_type(),
            description=game.description.as_generic_type(),
            release_date=game.release_date,
            developer=DeveloperDetailSchema.from_entity(game.developer),
            tags=[TagDetailSchema.from_entity(tag) for tag in game.tags],
            created_at=game.created_at
        )


class GetAllGamesQueryResponseSchema(BaseQueryResponseSchema[list[GameDetailForAllSchema]]):
    ...