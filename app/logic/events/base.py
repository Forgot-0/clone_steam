from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from domain.events.base import BaseEvent
from infra.message_broker.base import BaseMessageBroker


@dataclass(frozen=True)
class IntegrationEvent(BaseEvent, ABC):
    ...


ET = TypeVar('ET', bound=BaseEvent)
ER = TypeVar('ER', bound=Any)


@dataclass(frozen=True)
class BaseEventHandler(ABC, Generic[ET, ER]):
    message_broker: BaseMessageBroker
    broker_topic: str | None = None

    @abstractmethod
    async def handle(self, event: ET) -> ER:
        ...