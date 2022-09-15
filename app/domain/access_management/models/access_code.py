import uuid
from datetime import datetime
from typing import Optional, List

from enum import Enum
from sqlmodel import SQLModel, Relationship, Field

from app.domain.queue_management.models.queue import Queue


class Status(Enum):
    Waiting = 'WAITING'
    Attending = 'ATTENDING'
    Attended = 'ATTENDED'
    Skipped = 'SKIPPED'
    NotStarted = 'NOTSTARTED'

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


class RemainingCodes:
    remainingCodes: int


# class NextCodeCto:
#     accessCode: AccessCode(SQLModel)
#     remainingCodes: RemainingCodes


class CodeUuid(uuid.UUID):
    uuid: str


class AccessCode(SQLModel, table=True):
    id: int = Field(primary_key=True)
    modificationCounter: int
    code: str
    uuid: str
    createdDate: datetime
    startTime: datetime
    endTime: datetime
    status: str
    queueId: int

    #owner_id: str = Field(default=None, foreign_key="owner.id", nullable=True)
    #access_code: List['AccessCode'] = Relationship(back_populates="owner")

