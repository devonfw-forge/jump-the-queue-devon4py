import logging
from fastapi import APIRouter, Depends

from app.business.access_management.services.access import AccessCodeService

router = APIRouter(prefix="/access")

# getCurrentCode(): current> {
#       return this.http.post<AccessCode>(this.baseUrl + 'accesscodemanagement/v1/accesscode/current', {});
#     }


@router.post("/current", description="Gets ticket")
async def get_current_code(access_service: AccessCodeService = Depends(AccessCodeService)):
    access = await access_service.get_ticket_number()
    return access


@router.post("/next", description="Gets next ticket")
async def get_code_code(access_service: AccessCodeService = Depends(AccessCodeService)):
    access_new = await access_service.get_next_ticket_number()
    return access_new

@router.post("/uuid", description="Gets uuid")
async def get_uuid(access_service: AccessCodeService = Depends(AccessCodeService)):
    new_uuid = await access_service.get_uuid()
    return new_uuid


@router.post("/estimated", description="Get estimated time by code")
async def get_estimated_time(access_service: AccessCodeService = Depends(AccessCodeService)):
    estimated_time = await access_service.get_estimated_time()
    return estimated_time

@router.post("/estimated", description="Gets remaining codes count")
async def get_remaining_code(access_service: AccessCodeService = Depends(AccessCodeService)):
    remaining_code = await access_service.get_remaining_code()
    return remaining_code


