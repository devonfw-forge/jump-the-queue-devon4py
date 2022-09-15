from typing import Optional, List

from sqlmodel import SQLModel, Relationship

from app.common.base.base_entity import BaseUUIDModel
from app.domain.queue_management.models.queue import Queue


class Terms(BaseUUIDModel, table=True):
    title: str
    description: str

    #terms: Optional['Terms'] = Relationship(back_populates="access_code")
