from typing import Annotated
from uuid import UUID
from fastapi import Depends, status
from fastapi.routing import APIRouter

from application.api.developers.schemas.requests import ActivateDeveloperRequestSchema, CreateDeveloperRequestSchema
from application.api.developers.schemas.responses import DeveloperDetailSchema, GetAllDevelopersQueryResponseSchema
from application.api.schemas import ErrorSchema, Pagination
from application.dependencies import get_mediator
from logic.commands.developers.activate import ActivateEmailCommand
from logic.commands.developers.create import CreateDeveloperCommand
from logic.commands.developers.delete import DeleteDeveloperCommand
from logic.commands.developers.resend_activation_email import ResendActivationEmailCommand
from logic.mediator.mediator import Mediator
from logic.queries.developers.detail import DetailDeveloperQuery
from logic.queries.developers.get_all import GetAllDevelopersQuery


router = APIRouter(
    prefix='/developer',
    tags=['Developer']
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description='Create new developer',
    responses={
        status.HTTP_201_CREATED: {'model': DeveloperDetailSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def create_developer(
    schema: CreateDeveloperRequestSchema,
    mediator: Annotated[Mediator, Depends(get_mediator)]
) -> DeveloperDetailSchema:

    developer, *_ = await mediator.handle_command(
        CreateDeveloperCommand(**schema.model_dump())
    )

    return DeveloperDetailSchema.from_entity(developer=developer)

@router.delete(
    "/{developer_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    description='Delete developer',
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def delete_developer(
    developer_id: UUID,
    mediator: Annotated[Mediator, Depends(get_mediator)]
) -> None:

    await mediator.handle_command(
        DeleteDeveloperCommand(id=developer_id)
    )

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    description='Get all developers',
    responses={
        status.HTTP_200_OK: {'model': GetAllDevelopersQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def get_all_developers(
    mediator: Annotated[Mediator, Depends(get_mediator)],
    pagination: Pagination=Depends(),
) -> GetAllDevelopersQueryResponseSchema:

    items, count = await mediator.handle_query(
        GetAllDevelopersQuery(pagination=pagination.to_infra())
    )

    return GetAllDevelopersQueryResponseSchema(
        items=[DeveloperDetailSchema.from_entity(item) for item in items], 
        count=count,
        offset=pagination.offset,
        limit=pagination.limit)

@router.get(
    "/{developer_id}",
    status_code=status.HTTP_200_OK,
    description='Get developer',
    responses={
        status.HTTP_200_OK: {'model': DeveloperDetailSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def get_developer(
    developer_id: UUID,
    mediator: Annotated[Mediator, Depends(get_mediator)],
) -> DeveloperDetailSchema:

    developer = await mediator.handle_query(
        DetailDeveloperQuery(id=developer_id)
    )
    return DeveloperDetailSchema.from_entity(developer)

@router.post(
    '/activate',
    status_code=status.HTTP_204_NO_CONTENT,
    description="Activate developer",
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def activate(
    schema: ActivateDeveloperRequestSchema,
    mediator: Annotated[Mediator, Depends(get_mediator)],
) -> None:

    await mediator.handle_command(
        ActivateEmailCommand(**schema.model_dump())
    )

@router.post(
    '/resend_activation_email/{email}',
    status_code=status.HTTP_204_NO_CONTENT,
    description="Activate developer",
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def resend_email(
    email: str,
    mediator: Annotated[Mediator, Depends(get_mediator)],
) -> None:

    await mediator.handle_command(
        ResendActivationEmailCommand(email=email)
    )