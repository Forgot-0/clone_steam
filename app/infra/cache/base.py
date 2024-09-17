from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class BaseCacheService(ABC):

    @abstractmethod
    async def set_cache(self, key: str, data: str, time: int=60*60) -> None:
        ...

    @abstractmethod
    async def delete_cache(self, key: str) -> None:
        ...

    @abstractmethod
    async def get_cache(self, key: str) -> str:
        ...

    @abstractmethod
    async def get_or_set(self, key: str, data: str) -> str | None:
        ...


@dataclass
class MemoryCacheService(BaseCacheService):
    db: dict[str, str] = field(default_factory=dict)

    async def set_cache(self, key: str, data: str, time: int = 60 * 60):
        self.db[key] = data

    async def delete_cache(self, key: str) -> None:
        self.db.pop(key)

    async def get_cache(self, key: str) -> str:
        return self.db[key]

    async def get_or_set(self, key: str, data: str) -> str | None:
        data = self.db.get(key)
        if data: return data
        self.db[key] = data