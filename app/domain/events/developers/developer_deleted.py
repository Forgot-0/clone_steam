from dataclasses import dataclass
from uuid import UUID

from domain.events.base import BaseEvent


@dataclass(frozen=True)
class DeveloperDeleted(BaseEvent):
    id: UUID