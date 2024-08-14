from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from domain.events.base import BaseEvent
from infra.message_broker.base import BaseMessageBroker
from infra.message_broker.convertors import convert_event_to_broker_message


@dataclass(frozen=True)
class IntegrationEvent(BaseEvent, ABC):
    ...


ET = TypeVar('ET', bound=BaseEvent)
ER = TypeVar('ER', bound=Any)


@dataclass(frozen=True)
class BaseEventHandler(ABC, Generic[ET, ER]):
    message_broker: BaseMessageBroker
    broker_topic: str = 'game'

    @abstractmethod
    async def handle(self, event: ET) -> ER:
        ...


@dataclass(frozen=True)
class PublisherEventHandler(BaseEventHandler[BaseEvent, None]):

    async def handle(self, event: BaseEvent) -> None:
        await self.message_broker.send_message(
            topic='game',
            value=convert_event_to_broker_message(event=event),
            key=str(event.event_id).encode(),
        )