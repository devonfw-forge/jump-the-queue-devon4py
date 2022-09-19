from fastapi import APIRouter

from app.business.owner_management.router import owner_management_router
# Include all routers here

from app.business.queue_management.router import queue_management_router
from app.business.access_management.router import access_management_router


all_router = APIRouter()


all_router.include_router(queue_management_router)

all_router.include_router(access_management_router)

all_router.include_router(owner_management_router)