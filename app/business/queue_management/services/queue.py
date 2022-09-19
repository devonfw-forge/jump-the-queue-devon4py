from app.business.queue_management.models.queue import QueueDto
from app.domain.queue_management.models.queue import Queue


def parse_to_dto(queue_entity: Queue):
    return QueueDto(**queue_entity.dict())


class QueueService:
    async def get_todays_queue(self):
        pass

    async def start_queue(self):
        pass

