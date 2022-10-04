import logging

from fastapi import APIRouter, Depends
from typing import Optional
from app.business.queue_management.models.access import EstimatedTimeResponse, NextCodeCto, \
    RemainingCodes, UuidRequest, AccessCodeDto, AccessCodeResponse
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
    logger.info("Retrieve next ticket")
    return await access_service.get_next_ticket_number()


@router.post("/uuid", description="Get AccessCode by uuid creating visitors waiting", response_model=AccessCodeResponse)
async def get_access_code(request: UuidRequest, access_service: AccessCodeService = Depends(AccessCodeService)):
    logger.info("Retrieve current ticket")
    return await access_service.get_access_code(request.uuid)


@router.post("/estimated", description="Get estimated time by code", response_model=EstimatedTimeResponse)
async def get_estimated_time_by_code(request: AccessCodeDto, access_service: AccessCodeService = Depends(AccessCodeService)):
    logger.info("Retrieve estimated waiting time")
    attention_time_media = await access_service.get_estimated_time(request)
    return attention_time_media


@router.post("/remaining", description="Get remaining codes count", response_model=RemainingCodes)
async def get_remaining_codes_count(access_service: AccessCodeService = Depends(AccessCodeService)):
    logger.info("Retrieve the remaining ticket's amount")
    qty = await access_service.get_remaining_codes()
    return RemainingCodes(remainingCodes=qty)


@router.post("/leave", description="Leave the queue", response_model=AccessCodeDto)
async def leave_queue(request: UuidRequest, access_service: AccessCodeService = Depends(AccessCodeService)):
    logger.info("Retrieve the remaining ticket's amount")
    access_code = await access_service.leave_queue(request.uuid)
    return access_code

@router.get("/subscribe", description="Real time notifications")
async def subscribe(access_service: AccessCodeService = Depends(AccessCodeService)):
    return access_service.add_sse()
