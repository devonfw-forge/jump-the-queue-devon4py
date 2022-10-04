from datetime import date
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


##############################
#### classes status queue
###############################



class Direction(Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class SseTopic(Enum):
    QUEUE_STARTED = 'QUEUE_STARTED'
    NEW_CODE_ADDED = 'NEW_CODE_ADDED'
    CURRENT_CODE_CHANGED = 'CURRENT_CODE_CHANGED'
    CURRENT_CODE_CHANGED_NULL = 'CURRENT_CODE_CHANGED_NULL'


class QueueDto(BaseModel):
    id: int
    modificationCounter: int
    minAttentionTime: int
    started: bool
    createdDate: date





