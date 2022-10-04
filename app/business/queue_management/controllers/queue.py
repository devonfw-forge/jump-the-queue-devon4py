import logging
from fastapi import APIRouter, Depends
from app.business.queue_management.models.queue import QueueDto, TimeQueueDto
from app.business.queue_management.services.queue import QueueService

router = APIRouter(prefix="/queuemanagement/v1/queue")

logger = logging.getLogger(__name__)


@router.get("/daily/", description="Gets today queue", response_model=QueueDto)
async def get_todays_queue(queue_service: QueueService = Depends(QueueService)):
    return await queue_service.get_todays_queue()


@router.post("/start", description="Starting the queue", response_model=QueueDto)
async def start_queue(request: QueueDto, queue_service: QueueService = Depends(QueueService)):
    return await queue_service.start_queue(request.id)


@router.post("/time", description="Total waiting time for the queue", response_model=TimeQueueDto)
async def total_waiting_time(request: QueueDto, queue_service: QueueService = Depends(QueueService)):
    return await queue_service.waiting_queue_time(request.id)


@router.post("/close", description="Close the queue", response_model=QueueDto)
async def close_queue(request: QueueDto, queue_service: QueueService = Depends(QueueService)):
    return await queue_service.close_queue(request.id)
