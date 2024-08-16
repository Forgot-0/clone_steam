from dataclasses import dataclass
from typing import Any
from uuid import uuid4

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

    async def send_activation_developer_email(self, email: str) -> None:
        code = await self.generate_code(name=email)

        body = f"""{code}"""
        message_schema = conver_event_created_developer_to_message_schema(
            subject='Activation developer email',
            email=email,
            body=body
        )
        await self.fast_mail.send_message(message=message_schema)

    async def generate_code(self, name: str, time: int = 60*60):
        code = str(uuid4())

        await self.email_repository.set(
            name=name, 
            mapping={
                'code': code,
                'limit': 1,
                'resend': 1
            }
        )
        await self.email_repository.set_time(name=name, time=time)
        return code
