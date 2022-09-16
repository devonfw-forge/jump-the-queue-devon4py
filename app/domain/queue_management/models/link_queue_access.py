from typing import Optional
from uuid import UUID

from sqlmodel import Field

from app.common.base.base_entity import BaseUUIDModel


class Queue_AccessCode_Link(BaseUUIDModel, table=True):
    queue_id: Optional[UUID] = Field(
        default=None, foreign_key="queue.id", primary_key=True
    )
    access_code_id: Optional[UUID] = Field(
        default=None, foreign_key="access_code.id", primary_key=True
    )
