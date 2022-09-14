from typing import List

from sqlmodel import Relationship

from app.common.base.base_entity import *
from app.domain.queue_management.models.access_code import AccessCode
from app.domain.queue_management.models.queue import Queue


class Visitor(SQLModel, table=True):
    id: uuid_pkg.UUID = Field(
        default_factory=new_uuid,
        primary_key=True,
        index=True,
        nullable=False
    )
    userUID: str

    #queue: List[Queue] = Relationship(back_populates="visitor")
    #access: Optional[AccessCode] = Relationship(back_populates="visitor")