from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class CreateQueueRequest:
    async def get_queue(self):
        pass




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


class QueueDto(BaseModel):
    id: int
    modification_counter: int
    minAttention_time: int
    started: bool
    created_date: int




