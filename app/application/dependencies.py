from typing import Annotated

from fastapi import Depends
from punq import Container

from infra.depends.init import init_container
from logic.mediator.mediator import Mediator


def get_mediator(container: Annotated[Container, Depends(init_container)]) -> Mediator:
    mediator: Mediator = container.resolve(Mediator)
    return mediator
