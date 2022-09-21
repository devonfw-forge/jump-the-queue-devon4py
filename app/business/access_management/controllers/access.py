import logging
from typing import Optional

from fastapi import APIRouter, Depends
from app.business.access_management.models.access import EstimatedTimeResponse, AccessCodeDto, NextCodeCto, \
    RemainingCodes, UuidRequest, AccessCodeDto
from app.business.access_management.services.access import AccessCodeService

router = APIRouter(prefix="/accesscodemanagement/v1/accesscode")

logger = logging.getLogger(__name__)


@router.post("/current", description="Get current ticket", response_model=Optional[AccessCodeDto])
async def get_current_code(access_service: AccessCodeService = Depends(AccessCodeService)):
    logger.info("Retrieving current ticket")
    current_ticket = await access_service.get_current_ticket_number()
    return current_ticket


@router.post("/next", description="Get next ticket", response_model=NextCodeCto)
async def call_next_code(access_service: AccessCodeService = Depends(AccessCodeService)):
    pass
    # return await access_service.get_next_ticket_number(request)


@router.post("/uuid", description="Get uuid", response_model=AccessCodeDto)
async def get_code_by_uuid(request: UuidRequest, access_service: AccessCodeService = Depends(AccessCodeService)):
    pass
    # return await access_service.get_uuid(request)


@router.post("/estimated", description="Get estimated time by code", response_model=EstimatedTimeResponse)
async def get_estimated_time_by_code(request: AccessCodeDto,
                                     access_service: AccessCodeService = Depends(AccessCodeService)):
    pass
    # return await access_service.get_estimated_time(request)


@router.post("/remaining", description="Get remaining codes count", response_model=RemainingCodes)
async def get_remaining_codes_count(access_service: AccessCodeService = Depends(AccessCodeService)):
    pass
# return await access_service.get_remaining_code(request)
