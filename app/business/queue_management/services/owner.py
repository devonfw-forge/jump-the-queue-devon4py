import logging
from fastapi import Depends

from app.domain.queue_management.models.owner import Owner, Role
from app.domain.queue_management.repositories.owner import OwnerSQLRepository
from app.business.queue_management.models.owner import OwnerRequest, OwnerDto, OwnerResponse


def parse_to_dto(owner: Owner) -> OwnerResponse:
    owner_dto = None
    if owner:
        owner_dto = OwnerDto(
            id=owner.id,
            modificationCounter=0,
            username=owner.username,
            password=owner.password,
            userType=1 if owner.role == Role.Owner else 0
        )
    return OwnerResponse(
        content=[owner_dto]
    )


class OwnerService:

    def __init__(self, repository: OwnerSQLRepository = Depends(OwnerSQLRepository)):
        self.owner_repo = repository

    async def get_owner(self, owner_request: OwnerRequest) -> OwnerResponse:
        owner = await self.owner_repo.get_owner(owner_request.username, owner_request.password)
        return parse_to_dto(owner)
