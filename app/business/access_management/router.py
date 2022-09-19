from fastapi import APIRouter

from app.business.access_management.controllers import access
# Include all routers here

access_management_router = APIRouter()
access_management_router.include_router(access.router, tags=["Access"])
