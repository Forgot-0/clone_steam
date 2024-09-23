from dataclasses import dataclass
from domain.entities.base import BaseEntity
from domain.values.base import Slug, Title


@dataclass(eq=False)
class Language(BaseEntity):
    lang: Title
    slug: Slug
    interface: bool
    full_audio: bool
    subtitles: bool