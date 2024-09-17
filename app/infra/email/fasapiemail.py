from dataclasses import dataclass
from fastapi_mail import FastMail

from infra.email.base import BaseEmailBackend
from infra.email.convertors import conver_event_created_developer_to_message_schema
from infra.repositories.email.base import BaseEmailRepository





@dataclass
class FastApiEmailBackend(BaseEmailBackend):
    fast_mail: FastMail
    email_repository: BaseEmailRepository

    async def send_email(self, subject: str, email: str, body:str) -> None:
        message_schema = conver_event_created_developer_to_message_schema(
            subject=subject,
            email=email,
            body=body
        )
        await self.fast_mail.send_message(message=message_schema)