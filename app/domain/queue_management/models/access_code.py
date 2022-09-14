from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Relationship

from app.domain.queue_management.models.queue import Queue


class AccessCode(SQLModel, table=True):
    code: str
    createdTime: datetime
    startTime: datetime
    endTime: datetime

    queue: Optional[Queue] = Relationship(back_populates="my_access")
