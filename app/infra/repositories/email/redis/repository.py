from dataclasses import dataclass

from redis.asyncio import Redis

from infra.repositories.email.base import BaseEmailRepository
from infra.repositories.email.redis.convertors import convert_bytes_to_str


@dataclass
class RedisEmailRepository(BaseEmailRepository):
    redis: Redis

    async def set(self, name: str, mapping: dict) -> None:
        await self.redis.hmset(name=name, mapping=mapping)

    async def get(self, name: str, key: str) -> str:
        value = await self.redis.hget(name=name, key=key)
        return value

    async def set_time(self, name: str, time: int) -> None:
        await self.redis.expire(name=name, time=time)

    async def get_dict(self, name: str) -> dict[str, str] | None:
        value: dict[bytes, bytes] = await self.redis.hgetall(name=name)
        return convert_bytes_to_str(data=value)

    async def incr_by(self, name: str, key: str, amount: int) -> None:
        await self.redis.hincrby(name=name, key=key, amount=amount)

    async def delete(self, name: str) -> None:
        await self.redis.delete(name)

    async def set_for_time(self, name: str, mapping: dict, time: int = 60*60) -> None:
        await self.redis.hmset(name=name, mapping=mapping)
        await self.redis.expire(name=name, time=time)