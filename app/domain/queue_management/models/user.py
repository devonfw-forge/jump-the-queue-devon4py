from enum import Enum
from typing import Optional
from app.common.base.base_entity import new_uuid
import uuid as uuid_pkg
from sqlmodel import Field, SQLModel, Relationship


from app.domain.queue_management.models import *
from app.domain.queue_management.models.queue import Queue


class User(SQLModel, table=True):
    clientId: uuid_pkg.UUID = Field(
        default_factory=new_uuid,
        primary_key=True,
        index=True,
        nullable=False
    )
    username: str
    password: str

    role: Enum

    #queue: Optional[Queue] = Relationship(back_populates="user")