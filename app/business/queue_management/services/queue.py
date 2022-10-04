import logging

from fastapi import Depends

from app.business.queue_management.models.queue import QueueDto, SseTopic
from app.common.services.sse import EventPublisher
from app.domain.queue_management.models import Queue
from app.domain.queue_management.repositories.queue import QueueSQLRepository


def parse_to_dto(queue_entity: Queue):
    return QueueDto(
        id=queue_entity.id,
        modificationCounter=queue_entity.modificationCounter,
        minAttentionTime=queue_entity.min_attention_time,
        started=queue_entity.started,
        createdDate=queue_entity.created_date)


log = logging.getLogger(__name__)


class QueueService:
    queue_event_publisher = EventPublisher()

    def __init__(self, repository: QueueSQLRepository = Depends(QueueSQLRepository)):
        self.queue_repo = repository

    async def get_todays_queue(self) -> QueueDto:
        queue = await self.queue_repo.get_today_queue()
        if queue is None:
            queue = await self.queue_repo.create_queue()
        queue_dto = parse_to_dto(queue)

        return queue_dto

    async def start_queue(self, uid: int) -> QueueDto:
        """
        Start the Queue when is closed
        :param uid: the UID of the Queue
        :return: the Queue
        """
        current_queue = await self.queue_repo.get(uid=uid)
        if current_queue.started is False:
            current_queue.started = True
            await self.queue_repo.save(model=current_queue)
            self.queue_event_publisher.publish(data=parse_to_dto(current_queue).json(), topic=SseTopic.QUEUE_STARTED)
        else:
            log.info("Queue already started")
        return parse_to_dto(current_queue)
