from dataclasses import dataclass

from domain.events.developers.developer_created import NewDeveloperCreated
from infra.message_broker.convertors import convert_event_to_broker_message
from logic.events.base import BaseEventHandler



@dataclass(frozen=True)
class NewDeveloperCreatedEventHander(BaseEventHandler[NewDeveloperCreated, None]):
    async def handle(self, event: NewDeveloperCreated) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=str(event.event_id).encode(),
        )

