import logging
from fastapi import APIRouter, Depends
from typing import Optional
from app.business.queue_management.models.access import EstimatedTimeResponse, NextCodeCto, \
    RemainingCodes, UuidRequest, AccessCodeDto
from app.business.queue_management.services.access import AccessCodeService

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


@router.post("/uuid/", description="Get uuid", response_model=AccessCodeDto)
async def get_access_code(request: UuidRequest, access_service: AccessCodeService = Depends(AccessCodeService)):
    # comprobar si esta en la cola o no
    return await access_service.get_access_code(request.uuid)


@router.post("/estimated", description="Get estimated time by code", response_model=EstimatedTimeResponse)
async def get_estimated_time_by_code(request: AccessCodeDto,
                                     access_service: AccessCodeService = Depends(AccessCodeService)):
    pass
    # return await access_service.get_estimated_time(request)


@router.post("/remaining", description="Get remaining codes count", response_model=RemainingCodes)
async def get_remaining_codes_count(access_service: AccessCodeService = Depends(AccessCodeService)):
    qty = await access_service.get_remaining_codes()
    return RemainingCodes(remainingCodes=qty)
