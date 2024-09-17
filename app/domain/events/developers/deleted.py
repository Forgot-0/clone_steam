from dataclasses import dataclass
from uuid import UUID

from domain.events.base import BaseEvent


@dataclass(frozen=True)
class DeletedDeveloperEvent(BaseEvent):
    id: UUID