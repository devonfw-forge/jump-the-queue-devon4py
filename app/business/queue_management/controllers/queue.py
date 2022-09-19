import logging
from fastapi import APIRouter, Depends
from app.business.queue_management.services.queue import QueueService
from app.domain.queue_management.models import Queue

router = APIRouter(prefix="/queuemanagement/v1/queue")

logger = logging.getLogger(__name__)


@router.get("/daily", description="Gets today queue")
async def get_todays_queue(queue_service: QueueService = Depends(QueueService)):
    pass
    # todays_queue = await queue_service.get_todays_queue()


@router.post("/start", description="Starting the queue")
async def start_queue(queue_service: QueueService = Depends(QueueService)):
    pass
    # await queue_service.start_queue()


