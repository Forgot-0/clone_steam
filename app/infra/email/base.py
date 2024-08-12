from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, TypeVar



T = TypeVar("T", bound=Any)


@dataclass(frozen=True)
class EmailBackend(ABC):

    @abstractmethod
    async def send_email(self, template: dict[str, Any]) -> None:
        ...
