from dataclasses import dataclass
from typing import Iterable
from uuid import UUID

from app.domain.entities.developers import Developer
from app.infra.repositories.base import BaseMongoDBRepository
from app.infra.repositories.developer.base import BaseDeveloperRepository
from app.infra.repositories.filters import PaginationInfra


@dataclass
class MongoDeveloperRepository(BaseMongoDBRepository, BaseDeveloperRepository):

    async def check_exists_by_name(self, name: str) -> bool:
        ...

    
    async def check_exists_by_email(self, email: str) -> bool:
        ...

    
    async def create(self, developer: Developer) -> None:
        ...

    
    async def get_by_id(self, id: UUID) -> Developer | None:
        ...

    
    async def get_by_email(self, email: str) -> Developer | None:
        ...

    
    async def delete_by_id(self, id: UUID) -> None:
        ...

    
    async def update(self, developer: Developer) -> None:
        ...

    
    async def get_all(self, pagination: PaginationInfra) -> tuple[Iterable[Developer], int]:
        ...

    
    async def activate(self, id: UUID) -> None:
        ...
