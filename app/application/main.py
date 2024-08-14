from punq import Container
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from application.api.games.handlers import router as game_router
from application.api.developers.handlers import router as developer_router
from application.api.tags.handlers import router as tag_router
from application.api.languages.handlers import router as language_router
from application.lifespan import close_message_broker, init_message_broker



@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_message_broker()
    yield
    await close_message_broker()




def create_app() -> FastAPI:
    app = FastAPI(
        title='Game Store',
        docs_url='/api/docs',
        description='Clone steam',
        debug=True,
        lifespan=lifespan
    )

    app.include_router(game_router)
    app.include_router(developer_router)
    app.include_router(tag_router)
    app.include_router(language_router)

    return app