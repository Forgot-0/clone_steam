from dataclasses import dataclass
from typing import Iterable
from domain.entities.developers import Developer
from infra.repositories.developer.base import BaseDeveloperRepository
from infra.repositories.filters import PaginationInfra
from logic.queries.base import BaseQuery, BaseQueryHandler




@dataclass(frozen=True)
class GetAllDevelopersQuery(BaseQuery):
    pagination: PaginationInfra


@dataclass(frozen=True)
class GetAllDevelopersQueryHandler(BaseQueryHandler[GetAllDevelopersQuery, tuple[Iterable[Developer], int]]):
    developer_repository: BaseDeveloperRepository

    async def handle(self, query: GetAllDevelopersQuery) -> tuple[Iterable[Developer], int]:
        developers, count = await self.developer_repository.get_all(query.pagination)
        return developers, count