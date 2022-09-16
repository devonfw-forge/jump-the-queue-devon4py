from datetime import datetime
from enum import Enum
from uuid import UUID


class CreateQueueRequest:
    async def get_queue(self):
        pass


class QueueDto(CreateQueueRequest):
    id: UUID

##############################
#### classes status queue
###############################



class Direction(Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class SseTopic(Enum):
    QUEUE_STARTED = 'QUEUE_STARTED'
    CURRENT_CODE_CHANGED = 'CURRENT_CODE_CHANGED'
    CURRENT_CODE_CHANGED_NULL = 'CURRENT_CODE_CHANGED_NULL'

class EstimatedTime:
    miliseconds: datetime
    defaultTimeByUserInMs: datetime



