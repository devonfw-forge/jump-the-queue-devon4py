# import logging
from fastapi import APIRouter, Depends
from app.business.queue_management.models.owner import OwnerRequest, OwnerResponse
from app.business.queue_management.services.owner import OwnerService


router = APIRouter(prefix="/ownermanagement/v1/owner")


@router.post("/search", description="Gets owner", response_model=OwnerResponse)
async def get_owner(request: OwnerRequest, owner_service: OwnerService = Depends(OwnerService)):
    owner = await owner_service.get_owner(request)
    return owner
