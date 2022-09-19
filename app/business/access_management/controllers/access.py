import logging
from fastapi import APIRouter, Depends

from app.business.access_management.models.access import CodeRequest, UuidResponse, \
    EstimatedTimeResponse, AccessCodeResponse, NextCodeCto, RemainingCodes
from app.business.access_management.services.access import AccessCodeService

router = APIRouter(prefix="/accesscodemanagement/v1/accesscode")


@router.post("/current", description="Get ticket", response_model=AccessCodeResponse)
async def get_current_code(request: CodeRequest, access_service: AccessCodeService = Depends(AccessCodeService)):
    pass
    # return await access_service.get_ticket_number(request)


@router.post("/next", description="Get next ticket", response_model=NextCodeCto)
async def call_next_code(request: CodeRequest, access_service: AccessCodeService = Depends(AccessCodeService)):
    pass
    # return await access_service.get_next_ticket_number(request)


@router.post("/uuid", description="Get uuid", response_model=UuidResponse)
async def get_code_by_uuid(request: CodeRequest, access_service: AccessCodeService = Depends(AccessCodeService)):
    pass
    # return await access_service.get_uuid(request)


@router.post("/estimated", description="Get estimated time by code", response_model=EstimatedTimeResponse)
async def get_estimated_time_by_code(request: CodeRequest, access_service: AccessCodeService = Depends(AccessCodeService)):
    pass
    # return await access_service.get_estimated_time(request)


@router.post("/remaining", description="Get remaining codes count", response_model=RemainingCodes)
async def get_remaining_codes_count(request: CodeRequest, access_service: AccessCodeService = Depends(AccessCodeService)):
    pass
   # return await access_service.get_remaining_code(request)
