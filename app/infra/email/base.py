from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any



@dataclass
class BaseEmailBackend(ABC):

    @abstractmethod
    async def send_email(self, message: dict[str, Any]) -> None:
        ...

    @abstractmethod
    async def send_developer_activation_email(self, email: str) -> None:
        ...