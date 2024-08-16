from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseEmailRepository(ABC):

    @abstractmethod
    async def set(self, name: str, mapping: dict) -> None:
        ...

    @abstractmethod
    async def get(self, name: str, key: str) -> str:
        ...

    @abstractmethod
    async def set_time(self, name: str, time: int) -> None:
        ...

    @abstractmethod
    async def get_dict(self, name: str) -> dict:
        ...

    @abstractmethod
    async def incr_by(self,name: str, key: str, amount: int) -> None:
        ...

    @abstractmethod
    async def delete(self, name: str) -> None:
        ...