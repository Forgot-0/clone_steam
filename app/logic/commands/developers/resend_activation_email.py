from dataclasses import dataclass

from infra.email.base import BaseEmailBackend
from infra.repositories.email.base import BaseEmailRepository
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exeption import LimitResendActivationEmail, NotFoundException




@dataclass(frozen=True)
class ResendActivationEmailCommand(BaseCommand):
    email: str


@dataclass(frozen=True)
class ResendActivationEmailCommandHandler(BaseCommandHandler[ResendActivationEmailCommand, None]):
    email_backend: BaseEmailBackend
    email_repository: BaseEmailRepository

    async def handle(self, command: ResendActivationEmailCommand) -> None:
        email_data = await self.email_repository.get_dict(name=command.email)

        if not email_data and int(email_data['resend']) >= 3:
            raise LimitResendActivationEmail(name=command.email)

        await self.email_backend.send_developer_activation_email(email=command.email)

        await self.email_repository.incr_by(name=command.email, key='resend', amount=email_data['resend'])