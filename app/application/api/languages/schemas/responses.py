from uuid import UUID
from pydantic import BaseModel

from application.api.schemas import BaseQueryResponseSchema
from domain.entities.languages import Language




class LanguageDetailSchema(BaseModel):
    id: UUID
    lang: str
    slug: str
    interface: bool
    full_audio: bool
    subtitles: bool

    @classmethod
    def from_entity(cls, language: Language) -> 'LanguageDetailSchema':
        return cls(
            id=language.id,
            lang=language.lang.as_generic_type(),
            slug=language.slug.as_generic_type(),
            interface=language.interface,
            full_audio=language.full_audio,
            subtitles=language.subtitles,
        )


class GetAllLanguagesQueryResponseSchema(BaseQueryResponseSchema[list[LanguageDetailSchema]]):
    ...