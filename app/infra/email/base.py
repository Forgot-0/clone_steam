from abc import ABC, abstractmethod
from dataclasses import dataclass



@dataclass
class BaseEmailBackend(ABC):

    @abstractmethod
    async def send_email(self, subject: str, email: str, body:str) -> None:
        ...