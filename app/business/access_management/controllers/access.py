import logging
from fastapi import APIRouter, Depends

from app.business.access_management.models.access import CodeRequest, CodeResponse, CodeNextResponse, UuidResponse, \
    EstimatedTimeResponse, EstimatedCodeResponse
from app.business.access_management.services.access import AccessCodeService

router = APIRouter(prefix="/access")


@router.post("/current", description="Get ticket", response_model=CodeResponse)
async def get_current_code(request: CodeRequest, access_service: AccessCodeService = Depends(AccessCodeService)):
    pass
    # return await access_service.get_ticket_number(request)


@router.post("/next", description="Get next ticket", response_model=CodeNextResponse)
async def get_next_code(request: CodeRequest, access_service: AccessCodeService = Depends(AccessCodeService)):
    pass
    # return await access_service.get_next_ticket_number(request)


@router.post("/uuid", description="Get uuid", response_model=UuidResponse)
async def get_uuid(request: CodeRequest, access_service: AccessCodeService = Depends(AccessCodeService)):
    pass
    # return await access_service.get_uuid(request)


@router.post("/estimated", description="Get estimated time by code", response_model=EstimatedTimeResponse)
async def get_estimated_time(request: CodeRequest, access_service: AccessCodeService = Depends(AccessCodeService)):
    pass
    # return await access_service.get_estimated_time(request)


@router.post("/estimated", description="Get remaining codes count", response_model=EstimatedCodeResponse)
async def get_remaining_code(request: CodeRequest, access_service: AccessCodeService = Depends(AccessCodeService)):
    pass
   # return await access_service.get_remaining_code(request)
