from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel
from app.domain.access_management.models import AccessCode
from app.domain.access_management.models.access_code import Status


class AccessCodeDto(BaseModel):
    id: int
    code: str
    modificationCounter: int
    uuid: UUID
    created_time: datetime
    start_time: datetime
    end_time: datetime
    status: Status


class RemainingCodes(BaseModel):
    remainingCodes: int


class NextCodeCto(BaseModel):
    accessCode: AccessCode
    remainingCodes: RemainingCodes


class UuidRequest(BaseModel):
    uuid: str


class EstimatedTimeResponse(BaseModel):
    miliseconds: datetime
    defaultTimeByUserInMs: datetime


class AccessCodeStatus(Enum):
    WAITING = 'WAITING'
    ATTENDING = 'ATTENDING'
    ATTENDED = 'ATTENDED'
    SKIPPED = 'SKIPPED'
    NOTSTARTED = 'NOTSTARTED'
