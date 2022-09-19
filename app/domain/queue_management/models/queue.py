from uuid import UUID
from app.common.base.base_entity import *
from sqlmodel import Field


class Queue(BaseUUIDModel, table=True):
    name: str = Field(min_length=1)
    logo: Optional[str] = Field(min_length=1)
    description: Optional[str] = Field(min_length=1)
    access_link: str
    min_attention_time: datetime
    open_time: datetime
    close_time: datetime
    started: bool
    closed: bool

    fk_owner: UUID = Field(default=None, foreign_key="owner.id")
