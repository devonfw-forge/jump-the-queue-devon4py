from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
from sqlmodel import Field
from app.common.base.base_entity import BaseUUIDModel
from app.domain.owner_management.models import Visitor
from app.domain.queue_management.models import Queue


class Status(str, Enum):
    Waiting = 'WAITING'
    Attending = 'ATTENDING'
    Attended = 'ATTENDED'
    Skipped = 'SKIPPED'
    NotStarted = 'NOTSTARTED'


class AccessCode(BaseUUIDModel, table=True):
    code: str
    uuid: UUID
    created_time: datetime
    start_time: datetime
    end_time: datetime
    status: Status

    fk_queue: Optional['Queue'] = Field(default=None, foreign_key="queue.id")
    fk_visitor: Optional['Visitor'] = Field(default=None, foreign_key="visitor.id")

