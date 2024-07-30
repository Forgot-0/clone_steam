from dataclasses import dataclass
from domain.entities.base import BaseEntiy
from domain.values.base import Slug, Title


@dataclass(eq=False)
class Language(BaseEntiy):
    lang: Title
    slug: Slug
    interface: bool
    full_audio: bool
    subtitles: bool