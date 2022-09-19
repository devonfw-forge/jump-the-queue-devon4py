import logging
from fastapi import APIRouter, Depends
from app.business.access_management.services.access import *
from app.business.queue_management.services.queue import QueueService

router = APIRouter(prefix="/queue")

logger = logging.getLogger(__name__)




@router.get("/current", description="Gets today queue")
async def get_today_queue(queue_service: QueueService = Depends(QueueService)):
    #logger.info("Retrieving all the pending TODOs")
    queue  = await queue_service.get_queue()
    return queue


