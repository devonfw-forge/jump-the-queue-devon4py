from fastapi import APIRouter
from app.business.queue_management.router import queue_management_router

all_router = APIRouter()

# Include all routers here
all_router.include_router(queue_management_router)
