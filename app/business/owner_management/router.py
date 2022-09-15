from fastapi import APIRouter


# Include all routers here

from fastapi import APIRouter
# Include all routers here
from app.business.owner_management.controllers import owner
owner_management_router = APIRouter()
owner_management_router.include_router(owner.router, tags=["Owner"])

