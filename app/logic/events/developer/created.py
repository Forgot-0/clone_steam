from dataclasses import dataclass
from uuid import uuid4

from domain.events.developers.created import CreatedDeveloperEvent
from infra.email.base import BaseEmailBackend
from infra.repositories.email.base import BaseEmailRepository
from logic.events.base import BaseEventHandler



@dataclass(frozen=True)
class NewDeveloperCreatedEventHander(BaseEventHandler[CreatedDeveloperEvent, None]):
    email_backend: BaseEmailBackend
    email_repository: BaseEmailRepository

    async def handle(self, event: CreatedDeveloperEvent) -> None:
        code = str(uuid4())
        await self.email_repository.set_for_time(
            name=event.email,
            mapping={
                'code': code,
                'limit': 1,
                'resend': 1
            }
        )

        await self.email_backend.send_email(
            subject="Activation Developer Email",
            email=event.email, 
            body=f"{code}"
        )