from uuid import UUID
from app.common.base.base_entity import *
from sqlmodel import Field
from datetime import date

from app.common.utils import get_current_date


class Queue(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    modificationCounter: int = Field(default=0)
    min_attention_time: int = Field(default=120000)
    started: bool = Field(default=False)
    created_date: date = Field(default_factory=get_current_date)

    fk_owner: UUID = Field(default=None, foreign_key="owner.id")
