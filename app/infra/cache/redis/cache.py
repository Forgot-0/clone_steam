from dataclasses import dataclass
from json import loads

from redis.asyncio import Redis

from domain.entities.base import BaseEntity
from infra.cache.base import BaseCacheService
from infra.cache.redis.convertors import (
    convert_dict_to_entity, 
    convert_entities_to_list, 
    convert_entity_to_dict, 
    convert_list_to_entities
)



@dataclass
class RedisCacheService(BaseCacheService):
    redis: Redis

    async def set(self, key: str, value: BaseEntity | list[BaseEntity], time: int=60*60, count: int=0) -> None:
        if isinstance(value, BaseEntity):
            data = convert_entity_to_dict(entity=value)
        else:
            data = convert_entities_to_list(entities=value, count=count)

        await self.redis.set(name=key, value=data, ex=time)

    async def delete_cache(self, key: str) -> None:
        await self.redis.delete(key)

    async def get_cache(self, key: str, type_cls: BaseEntity) -> BaseEntity | list[BaseEntity] | None:
        data = loads(await self.redis.get(name=key))

        if not data: return

        if isinstance(data, dict):
            return convert_dict_to_entity(data, type_cls=type_cls)
        return convert_list_to_entities(data, type_cls=type_cls)

    def key_builder(*args, **kwargs) -> str:
        return f'{args}-{kwargs}'


