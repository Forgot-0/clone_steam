from dataclasses import dataclass
from domain.entities.base import BaseEntiy
from domain.values.base import Slug, Title


@dataclass(eq=False)
class Tag(BaseEntiy):
    name: Title
    slug: Slug
