from fastapi import APIRouter
# Include all routers here
from app.business.queue_management.controllers import queue
queue_management_router = APIRouter()
queue_management_router.include_router(queue.router, tags=["Queue"])
