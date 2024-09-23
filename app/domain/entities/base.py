from abc import ABC
from copy import copy
from dataclasses import dataclass, field
from uuid import UUID, uuid4

from domain.events.base import BaseEvent




@dataclass
class BaseEntity(ABC):
    id: UUID = field(
        default_factory=lambda: uuid4(),
        kw_only=True
    )
    # id: int = field(default=0)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, __value: 'BaseEntity') -> bool:
        return self.id == __value.id


@dataclass(kw_only=True)
class AggregateRoot(BaseEntity, ABC):
    _events: list[BaseEvent] = field(
        default_factory=list,
        init=False, repr=False, hash=False, compare=False,
    )

    def register_event(self, event: BaseEvent) -> None:
        self._events.append(event)

    def pull_events(self) -> list[BaseEvent]:
        registered_events = copy(self._events)
        self._events.clear()

        return registered_events