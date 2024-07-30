from dataclasses import dataclass
from uuid import UUID
from domain.entities.developers import Developer
from infra.repositories.developer.base import BaseDeveloperRepository
from logic.exeption import NotFoundException
from logic.queries.base import BaseQuery, BaseQueryHandler




@dataclass(frozen=True)
class DetailDeveloperQuery(BaseQuery):
    id: UUID


@dataclass(frozen=True)
class DetailDevelopersQueryHandler(BaseQueryHandler[DetailDeveloperQuery, Developer]):
    developer_repository: BaseDeveloperRepository

    async def handle(self, query: DetailDeveloperQuery) -> Developer:
        developer = await self.developer_repository.get_by_id(id=query.id)
        
        if not developer:
            raise NotFoundException('Not found developer by id')

        return developer