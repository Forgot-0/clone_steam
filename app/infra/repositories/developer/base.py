from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterable
from uuid import UUID

from domain.entities.developers import Developer
from infra.repositories.filters import PaginationInfra



@dataclass
class BaseDeveloperRepository(ABC):

    @abstractmethod
    async def check_exists_by_name(self, name: str) -> bool:
        ...

    @abstractmethod
    async def check_exists_by_email(self, email: str) -> bool:
        ...

    @abstractmethod
    async def create(self, developer: Developer) -> None:
        ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Developer | None:
        ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Developer | None:
        ...

    @abstractmethod
    async def delete_by_id(self, id: UUID) -> None:
        ...

    @abstractmethod
    async def update(self, developer: Developer) -> None:
        ...

    @abstractmethod
    async def get_all(self, pagination: PaginationInfra) -> tuple[Iterable[Developer], int]:
        ...

    @abstractmethod
    async def activate(self, id: UUID) -> None:
        ...


@dataclass
class MemoryDeveloperRepository(BaseDeveloperRepository):

    db: list[Developer] = field(default_factory=list, kw_only=True)

    async def check_exists_by_name(self, name: str) -> bool:
        for developer in self.db:
            if developer.name.as_generic_type() == name:
                return True
        return False

    async def check_exists_by_email(self, email: str) -> bool:
        for developer in self.db:
            if developer.email.as_generic_type() == email:
                return True
        return False

    async def create(self, developer: Developer) -> None:
        self.db.append(developer)

    async def get_by_id(self, id: UUID) -> Developer | None:
        for developer in self.db:
            if developer.id == id:
                if developer.is_deleted:
                    return None
                return developer
        return None

    async def get_by_email(self, email: str) -> Developer | None:
        for developer in self.db:
            if developer.email.as_generic_type() == email:
                return developer
        return None

    async def delete_by_id(self, id: UUID) -> None:
        for i, developer in enumerate(self.db):
            if developer.id == id:
                break

        self.db.pop(i)

    async def update(self, developer: Developer) -> None:
        for i in range(len(self.db)):
            if developer.id == self.db[i].id:
                self.db[i] = developer
                break

    async def get_all(self, pagination: PaginationInfra) -> Iterable[Developer]:
        return list(
            filter(
                lambda el: not el.is_deleted, 
                self.db[pagination.offset:pagination.limit]
                )
            ), len(self.db)

    async def activate(self, id: UUID) -> None:
        for dev in self.db:
            if dev.id == id:
                dev.is_active = True
                return
