from dataclasses import dataclass

from redis.asyncio import Redis

from infra.repositories.email.base import BaseEmailRepository


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

    async def get_dict(self, name: str) -> dict:
        value: dict[bytes, bytes] = await self.redis.hgetall(name=name)
        return {key.decode('utf-8'): value.decode('utf-8') for key, value in value.items()}

    async def incr_by(self, name: str, key: str, amount: int) -> None:
        await self.redis.hincrby(name=name, key=key, amount=amount)

    async def delete(self, name: str) -> None:
        await self.redis.delete(name)