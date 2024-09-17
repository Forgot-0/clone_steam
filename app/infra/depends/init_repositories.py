from redis.asyncio import Redis
from infra.repositories.developer.mongo.repository import MongoDeveloperRepository
from infra.repositories.email.redis.repository import RedisEmailRepository
from infra.repositories.game.mongo.repository import MongoGameRepository
from infra.repositories.languages.mongo.repository import MongoLanguageRepository
from infra.repositories.tags.mongo.repository import MongoTagRepository
from motor.motor_asyncio import AsyncIOMotorClient


def init_redis_email_repository(redis: Redis):
    return RedisEmailRepository(
        redis=redis
    )

def init_mongo_developer_repository(client: AsyncIOMotorClient):
    return MongoDeveloperRepository(
        mongo_db_client=client,
        mongo_db_db_name='test',
        mongo_db_collection_name='developers',
    )

def init_mongo_game_repository(client: AsyncIOMotorClient):
    return MongoGameRepository(
        mongo_db_client=client,
        mongo_db_db_name='test',
        mongo_db_collection_name='games',
    )

def init_mongo_tag_repository(client: AsyncIOMotorClient):
    return MongoTagRepository(
        mongo_db_client=client,
        mongo_db_db_name='test',
        mongo_db_collection_name='tags'
    )

def init_mongo_language_repository(client: AsyncIOMotorClient):
    return MongoLanguageRepository(
        mongo_db_client=client,
        mongo_db_db_name='test',
        mongo_db_collection_name='languages'
    )
