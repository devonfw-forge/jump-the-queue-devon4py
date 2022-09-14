from typing import Optional

from sqlmodel import SQLModel, Relationship

from app.domain.queue_management.models.queue import Queue


class Terms(SQLModel, table=True):
    title: str
    description: str

   # queue: Optional[Queue] = Relationship(back_populates="terms")
