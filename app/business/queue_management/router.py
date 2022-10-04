from fastapi import APIRouter
# Include all routers here
from app.business.queue_management.controllers import queue, access, owner

queue_management_router = APIRouter(prefix="/services/rest")
queue_management_router.include_router(queue.router, tags=["Queue"])
queue_management_router.include_router(access.router, tags=["Access"])
queue_management_router.include_router(owner.router, tags=["Owner"])


