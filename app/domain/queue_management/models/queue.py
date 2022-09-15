from typing import List
from uuid import UUID

from app.common.base.base_entity import *
from sqlmodel import Relationship, SQLModel, Field




class Queue(BaseUUIDModel, table=True):
    name: str = Field(min_length=1)
    logo: Optional[str] = Field(min_length=1)
    description: Optional[str] = Field(min_length=1)
    accesslink: str
    minAttentionTime: datetime
    openTime: datetime
    closeTime: datetime
    started: bool
    closed: bool
    createdDate: datetime

    fk_owner: UUID = Field(default=None, foreign_key="owner.id")

    #queue: List['Queue'] = Relationship(back_populates="access_code")

