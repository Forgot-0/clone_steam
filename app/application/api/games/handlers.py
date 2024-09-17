from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status

from application.api.games.schemas.requests import CreateGameRequestSchema, GameFilters
from application.api.games.schemas.responses import (
    GameDetailForAllSchema, 
    GameDetailSchema,
    GetAllGamesQueryResponseSchema
)
from application.api.schemas import ErrorSchema, Pagination
from application.dependencies import get_mediator
from logic.commands.games.create import CreateGameCommand
from logic.commands.games.delete import DeleteGameCommand
from logic.mediator.mediator import Mediator
from logic.queries.games.detail import DetailGameQuery
from logic.queries.games.get_all import GetAllGameQuery
from logic.queries.games.get_games import GetGamesFilterQuery


router = APIRouter(
    prefix='/game',
    tags=['Game'],
)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    description='Create game',
    responses={
        status.HTTP_201_CREATED: {'model': GameDetailSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def create_game(
    schema: CreateGameRequestSchema,
    mediator: Annotated[Mediator, Depends(get_mediator)]
) -> GameDetailSchema:

    game, *_ = await mediator.handle_command(
        CreateGameCommand(**schema.model_dump())
    )

    return GameDetailSchema.from_entity(game=game)

@router.get(
    '/{game_id}',
    status_code=status.HTTP_200_OK,
    description='Get game by id',
    responses={
        status.HTTP_200_OK: {'model': GameDetailSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def get_game_by_id(
    game_id: UUID,
    mediator: Annotated[Mediator, Depends(get_mediator)]
) -> GameDetailSchema:

    developer = await mediator.handle_query(
        DetailGameQuery(game_id=game_id)
    )

    return GameDetailSchema.from_entity(developer)

@router.delete(
    '/{game_id}',
    status_code=status.HTTP_200_OK,
    description='Delete game by id',
    responses={
        status.HTTP_200_OK: {'model': GameDetailSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def delete_game_by_id(
    game_id: UUID,
    mediator: Annotated[Mediator, Depends(get_mediator)]
) -> GameDetailSchema:

    developer = await mediator.handle_command(
        DeleteGameCommand(game_id=game_id)
    )
    
    return GameDetailSchema.from_entity(developer)

@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    description='Get all game',
    responses={
        status.HTTP_200_OK: {'model': GetAllGamesQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def get_all_games(
    mediator: Annotated[Mediator, Depends(get_mediator)],
    pagination: Pagination=Depends(),
) -> GetAllGamesQueryResponseSchema:

    games, count = await mediator.handle_query(
        GetAllGameQuery(pagination=pagination.to_infra())
    )
   
    return GetAllGamesQueryResponseSchema(
        items=[GameDetailForAllSchema.from_entity(game) for game in games],
        count=count,
        offset=pagination.offset,
        limit=pagination.limit,
    )

@router.get(
    '/search/',
    status_code=status.HTTP_200_OK,
    description='Get games',
    responses={
        status.HTTP_200_OK: {'model': GetAllGamesQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def get_games(
    mediator: Annotated[Mediator, Depends(get_mediator)],
    filters: GameFilters=Depends(),
    pagination: Pagination=Depends(),
    tags: list[UUID]=Query(default_factory=list),
    languages: list[UUID]=Query(default_factory=list),
) -> GetAllGamesQueryResponseSchema:

    games, count = await mediator.handle_query(
        GetGamesFilterQuery(
            filters=filters.to_infra(tags=tags, languages=languages), 
            pagination=pagination.to_infra()
        )
    )
    
    return GetAllGamesQueryResponseSchema(
        items=[GameDetailForAllSchema.from_entity(game) for game in games],
        count=count,
        offset=pagination.offset,
        limit=pagination.limit,
    )