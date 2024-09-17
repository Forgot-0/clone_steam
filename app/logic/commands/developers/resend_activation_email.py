from dataclasses import dataclass
from uuid import uuid4

from infra.email.base import BaseEmailBackend
from infra.repositories.email.base import BaseEmailRepository
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exeption import LimitResendActivationEmail




@dataclass(frozen=True)
class ResendActivationEmailCommand(BaseCommand):
    email: str


@dataclass(frozen=True)
class ResendActivationEmailCommandHandler(BaseCommandHandler[ResendActivationEmailCommand, None]):
    email_backend: BaseEmailBackend
    email_repository: BaseEmailRepository

    async def handle(self, command: ResendActivationEmailCommand) -> None:
        email_data = await self.email_repository.get_dict(name=command.email)

        if email_data and int(email_data['resend']) >= 3:
            raise LimitResendActivationEmail(name=command.email)

        code = str(uuid4())

        await self.email_repository.set_for_time(
            name=command.email,
            mapping={
                'code': code,
                'limit': 1,
                'resend': email_data['resend'] + 1 if email_data else 1
            }
        )

        await self.email_backend.send_email(
            subject="Activation Developer Email",
            email=command.email, 
            body=f"{code}"
        )