from dataclasses import dataclass
from uuid import UUID

from domain.events.base import BaseEvent


@dataclass(frozen=True)
class CreatedDeveloperEvent(BaseEvent):
    id: UUID
    name: str
    slug: str
    email: str
