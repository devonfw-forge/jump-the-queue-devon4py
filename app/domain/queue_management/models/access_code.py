from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
from sqlmodel import Field
from app.common.base.base_entity import BaseUUIDModel
from app.common.utils import get_current_time


class Status(str, Enum):
    Waiting = 'WAITING'
    Attending = 'ATTENDING'
    Attended = 'ATTENDED'
    Skipped = 'SKIPPED'
    NotStarted = 'NOTSTARTED'


class AccessCode(BaseUUIDModel, table=True):
    code: str
    modification_counter: int = Field(default=0)
    created_time: datetime = Field(default_factory=get_current_time)
    start_time: Optional[datetime] = Field(default=None)
    end_time: Optional[datetime] = Field(default=None)
    status: Status = Field(default=Status.Waiting)

    fk_queue: Optional[int] = Field(default=None, foreign_key="queue.id")
    fk_visitor: Optional[UUID] = Field(default=None, foreign_key="visitor.id")

