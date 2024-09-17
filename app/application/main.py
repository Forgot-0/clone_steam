from fastapi import FastAPI, HTTPException, Request, status
from fastapi.concurrency import asynccontextmanager

from application.api.healthchecks import router as healthchecks_router
from application.api.games.handlers import router as game_router
from application.api.developers.handlers import router as developer_router
from application.api.tags.handlers import router as tag_router
from application.api.languages.handlers import router as language_router
from application.lifespan import close_message_broker, init_message_broker
from domain.exception.base import ApplicationException



async def handle_application_exception(
    request: Request, exception: ApplicationException
) -> None:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})


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

    app.include_router(healthchecks_router)
    app.include_router(game_router)
    app.include_router(developer_router)
    app.include_router(tag_router)
    app.include_router(language_router)
    app.add_exception_handler(ApplicationException, handle_application_exception)

    return app