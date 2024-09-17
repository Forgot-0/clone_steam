from dataclasses import dataclass

from infra.email.base import BaseEmailBackend
from infra.repositories.developer.base import BaseDeveloperRepository
from infra.repositories.email.base import BaseEmailRepository
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exeption import LimitExceeded, WrongException




@dataclass(frozen=True)
class ActivateEmailCommand(BaseCommand):
    email: str
    code: str


@dataclass(frozen=True)
class ActivateEmailCommandHandler(BaseCommandHandler[ActivateEmailCommand, None]):
    developer_repository: BaseDeveloperRepository
    email_repository: BaseEmailRepository

    async def handle(self, command: ActivateEmailCommand) -> None:
        email_data = await self.email_repository.get_dict(name=command.email)

        if int(email_data['limit']) > 3:
            raise LimitExceeded(f"{command.email}")

        if email_data['code'] != command.code:
            await self.email_repository.incr_by(name=command.email, key='limit', amount=1)
            raise WrongException("Wrong code")

        await self.email_repository.delete(name=command.email)
        await self.developer_repository.activate(email=command.email)
