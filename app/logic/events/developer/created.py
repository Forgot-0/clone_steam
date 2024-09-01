from dataclasses import dataclass

from domain.events.developers.developer_created import NewDeveloperCreated
from infra.email.base import BaseEmailBackend
from logic.events.base import BaseEventHandler



@dataclass(frozen=True)
class NewDeveloperCreatedEventHander(BaseEventHandler[NewDeveloperCreated, None]):
    email_backend: BaseEmailBackend

    async def handle(self, event: NewDeveloperCreated) -> None:
        await self.email_backend.send_developer_activation_email(email=event.email)

