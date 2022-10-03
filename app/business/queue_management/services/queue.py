import logging

from fastapi import Depends

from app.business.queue_management.models.queue import QueueDto, TimeQueueDto
from app.domain.queue_management.models import Queue
from app.domain.queue_management.repositories.access_code import AccessCodeSQLRepository
from app.domain.queue_management.repositories.queue import QueueSQLRepository


def parse_to_dto(queue_entity: Queue):
    return QueueDto(
        id=queue_entity.id,
        modificationCounter=queue_entity.modificationCounter,
        minAttentionTime=queue_entity.min_attention_time,
        started=queue_entity.started,
        createdDate=queue_entity.created_date)


def parse_to_time_dto(queue_entity: Queue, total_time: int):
    return TimeQueueDto(
        id=queue_entity.id,
        modificationCounter=queue_entity.modificationCounter,
        minAttentionTime=queue_entity.min_attention_time,
        totalAttentionTime= total_time,
        started=queue_entity.started,
        createdDate=queue_entity.created_date)


log = logging.getLogger(__name__)


class QueueService:

    def __init__(self, repository: QueueSQLRepository = Depends(QueueSQLRepository),
                 access_code_repo: AccessCodeSQLRepository = Depends(AccessCodeSQLRepository)):
        self.queue_repo = repository
        self.access_code_repo = access_code_repo

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
        else:
            log.info("Queue already started")
        return parse_to_dto(current_queue)

    async def waiting_queue_time(self, queue_id: int) -> TimeQueueDto:
        current_queue = await self.queue_repo.get(uid=queue_id)
        attended_customers_times = await self.access_code_repo.get_access_code_attended(current_queue.id)
        attention_time = list(map(lambda x: x[0] - x[1] if x[0] - x[1] >= current_queue.min_attention_time else current_queue.min_attention_time, attended_customers_times))
        try:
            average_attention_time = sum(attention_time)/len(attention_time)
        except ZeroDivisionError:
            average_attention_time = 12000
        nb_waiting_customers = await self.access_code_repo.get_waiting_customers_count(current_queue.id)
        total_waiting_time = len(nb_waiting_customers) * average_attention_time

        return parse_to_time_dto(current_queue, total_waiting_time)

    async def close_queue(self, uid: int) -> QueueDto:
        """
        Close the Queue when is started
        :param uid: the UID of the Queue
        :return: the Queue
        """
        current_queue = await self.queue_repo.get(uid=uid)
        if current_queue.started is True:
            current_queue.started = False
            await self.queue_repo.save(model=current_queue)
        else:
            log.info("Queue already closed")
        return parse_to_dto(current_queue)

