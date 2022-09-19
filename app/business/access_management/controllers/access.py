import logging
from fastapi import APIRouter, Depends

from app.business.access_management.models.access import CodeRequest
from app.business.access_management.services.access import AccessCodeService

router = APIRouter(prefix="/access")


@router.post("/current", description="Gets ticket")
async def get_current_code(request: CodeRequest, access_service: AccessCodeService = Depends(AccessCodeService)):
    return await access_service.get_ticket_number(request)


@router.post("/next", description="Gets next ticket")
async def get_next_code(request: CodeRequest, access_service: AccessCodeService = Depends(AccessCodeService)):
    return await access_service.get_next_ticket_number(request)


@router.post("/uuid", description="Gets uuid")
async def get_uuid(request: CodeRequest, access_service: AccessCodeService = Depends(AccessCodeService)):
    return await access_service.get_uuid(request)


@router.post("/estimated", description="Get estimated time by code")
async def get_estimated_time(request: CodeRequest, access_service: AccessCodeService = Depends(AccessCodeService)):
    return await access_service.get_estimated_time(request)


@router.post("/estimated", description="Gets remaining codes count")
async def get_remaining_code(request: CodeRequest, access_service: AccessCodeService = Depends(AccessCodeService)):
    return await access_service.get_remaining_code(request)
