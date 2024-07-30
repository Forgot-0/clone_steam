from typing import Generic, TypeVar
from pydantic import BaseModel

from infra.repositories.filters import PaginationInfra




class ErrorSchema(BaseModel):
    error: str


class OkResponse(BaseModel):
    status: int = 200


IT = TypeVar('IT')


class BaseQueryResponseSchema(BaseModel, Generic[IT]):
    count: int
    offset: int
    limit: int
    items: IT


class Pagination(BaseModel):
    offset: int = 0
    limit: int = 10

    def to_infra(self):
        return PaginationInfra(limit=self.limit, offset=self.offset)