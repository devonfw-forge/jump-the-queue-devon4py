from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel
from typing import Optional
from app.domain.queue_management.models.access_code import Status, AccessCode


class AccessCodeDto(BaseModel):
    id: UUID
    modificationCounter: int
    code: str
    uuid: UUID
    createdDate: datetime
    starTime: Optional[datetime]
    endTime: Optional[datetime]
    status: Status
    queueId: int


class RemainingCodes(BaseModel):
    remainingCodes: int


class NextCodeCto(BaseModel):
    accessCode: AccessCode
    remainingCodes: RemainingCodes


class UuidRequest(BaseModel):
    uuid: UUID


class EstimatedTimeResponse(BaseModel):
    miliseconds: datetime
    defaultTimeByUserInMs: datetime


class AccessCodeStatus(Enum):
    WAITING = 'WAITING'
    ATTENDING = 'ATTENDING'
    ATTENDED = 'ATTENDED'
    SKIPPED = 'SKIPPED'
    NOTSTARTED = 'NOTSTARTED'






