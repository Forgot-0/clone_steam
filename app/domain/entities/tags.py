from dataclasses import dataclass
from domain.entities.base import BaseEntity
from domain.values.base import Slug, Title


@dataclass(eq=False)
class Tag(BaseEntity):
    name: Title
    slug: Slug
