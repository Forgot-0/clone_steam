from functools import lru_cache
from punq import Container
from logic.depends.container import _init_container

@lru_cache(1)
def init_container() -> Container:
    return _init_container()
