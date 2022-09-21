from fastapi import Depends
from app.business.queue_management.models.queue import QueueDto
from app.domain.queue_management.models import Queue
from app.domain.queue_management.repositories.queue import QueueSQLRepository


def parse_to_dto(queue_entity: Queue):
    return QueueDto(id=queue_entity.id, modificationCounter=queue_entity.modificationCounter,
                    minAttentionTime=queue_entity.min_attention_time, started=queue_entity.started,
                    createdDate=queue_entity.created_date)


class QueueService:

    def __init__(self, repository: QueueSQLRepository = Depends(QueueSQLRepository)):
        self.queue_repo = repository

    async def get_todays_queue(self) -> QueueDto:
        queue = await self.queue_repo.get_today_queue()
        if queue is None:
            queue = await self.queue_repo.create_queue()
        queue_dto = parse_to_dto(queue)

        return queue_dto

    async def start_queue(self, request):
        # TODO: started a True ver la US de start queue
        pass
