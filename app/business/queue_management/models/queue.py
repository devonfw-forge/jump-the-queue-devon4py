from uuid import UUID


class CreateQueueRequest:
    async def get_queue(self):
        pass


class QueueDto(CreateQueueRequest):
    id: UUID


