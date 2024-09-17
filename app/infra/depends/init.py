from functools import lru_cache
from punq import Container
from infra.depends.container import _init_container
from logic.mediator.mediator import Mediator



@lru_cache(1)
def init_container() -> Container:
    return _init_container()
