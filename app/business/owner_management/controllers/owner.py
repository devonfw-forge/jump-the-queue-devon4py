# import logging


# from fastapi import APIRouter, Depends
# from app.business.owner_management.services.owner import OwnerService
#
#
# router = APIRouter(prefix="/owner")
#
#
# @router.get("/owner-role", description="Gets owner")
# async def get_owner(owner_service: OwnerService = Depends(OwnerService)):
#     owner = await owner_service.get_owner()
#     return owner
# @router.post("/owner-role/{username}/{password}/", description="Gets owner")
# async def create_owner(username: str, password: str, request: CreateOwnerRequest, owner_service: OwnerService = Depends(OwnerService)):
# @router.get("/employees", description="Gets Employees")
# async def get_employees(owner_service: OwnerService = Depends(OwnerService)):
#     employees = await owner_service.get_employees()
#     return list[employees]
