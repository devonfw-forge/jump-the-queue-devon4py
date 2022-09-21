import logging
from fastapi import APIRouter, Depends
from app.business.queue_management.models.queue import QueueDto
from app.business.queue_management.services.queue import QueueService

router = APIRouter(prefix="/queuemanagement/v1/queue")

logger = logging.getLogger(__name__)


@router.get("/daily", description="Gets today queue", response_model=QueueDto)
async def get_todays_queue(queue_service: QueueService = Depends(QueueService)):
    return await queue_service.get_todays_queue()


@router.post("/start", description="Starting the queue", response_model=QueueDto)
async def start_queue(request: QueueDto, queue_service: QueueService = Depends(QueueService)):
    return await queue_service.start_queue(request.id)
