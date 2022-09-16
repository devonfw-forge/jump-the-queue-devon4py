import uuid
from datetime import datetime
from typing import Optional, List

from enum import Enum
from sqlmodel import SQLModel, Relationship, Field

from app.common.base.base_entity import BaseUUIDModel
from app.domain.queue_management.models.queue import Queue


# class NextCodeCto:
#     accessCode: AccessCode(SQLModel)
#     remainingCodes: RemainingCodes


class AccessCode(BaseUUIDModel, table=True):
    modificationCounter: int
    code: str
    uuid: str
    createdDate: datetime
    startTime: datetime
    endTime: datetime
    status: str
    queueId: int

    access_code: List['AccessCode'] = Relationship(back_populates="owner")

