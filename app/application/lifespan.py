from infra.message_broker.base import BaseMessageBroker
from infra.depends.init import init_container
from logic.mediator.mediator import Mediator
from settings.config import Config


async def init_message_broker() -> None:
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.start()

async def consume_in_background() -> None:
    container = init_container()
    config: Config = container.resolve(Config)
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)

    mediator: Mediator = container.resolve(Mediator)

    pass

async def close_message_broker() -> None:
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.close()