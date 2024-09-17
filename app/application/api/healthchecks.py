from fastapi import APIRouter, status

from application.api.schemas import ErrorSchema, OkResponse


router = APIRouter(
    prefix="/healthcheck",
    tags=["healthcheck"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    description='healthcheck',
    responses={
        status.HTTP_200_OK: {'model': OkResponse},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def healthcheck() -> OkResponse:
    return OkResponse()