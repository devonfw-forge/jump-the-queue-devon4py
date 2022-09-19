import datetime
import logging
from typing import Optional

from fastapi import APIRouter, Depends

from app.business.queue_management.models.queue import QueueDto
from app.business.queue_management.services.queue import QueueService
from app.domain.queue_management.models import Queue

router = APIRouter(prefix="/queuemanagement/v1/queue")

logger = logging.getLogger(__name__)

# name: str = Field(min_length=1)
# logo: Optional[str] = Field(min_length=1)
# description: Optional[str] = Field(min_length=1)
# access_link: str
# min_attention_time: datetime
# open_time: datetime
# close_time: datetime
# started: bool
# closed: bool
@router.get("/daily", description="Gets today queue", response_model=QueueDto)
async def get_todays_queue(queue_service: QueueService = Depends(QueueService)):
    return await queue_service.get_todays_queue()


@router.post("/start", description="Starting the queue", response_model=QueueDto)
async def start_queue(request: QueueDto,  queue_service: QueueService = Depends(QueueService)):
    return await queue_service.start_queue(request)


