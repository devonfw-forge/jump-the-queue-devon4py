from enum import Enum
from typing import Optional, List
from uuid import UUID

from app.common.base.base_entity import new_uuid, BaseUUIDModel

from sqlmodel import Field, SQLModel, Relationship
from app.common.base.base_repository import BaseSQLRepository
from app.common.exceptions.http import NotFoundException
from app.common.infra.sql_adaptors import get_session, get_async_session, AsyncSession

from app.domain.queue_management.models import *
from app.domain.queue_management.models.queue import *


class Owner(BaseUUIDModel, table=True):
    username: str
    password: str
    userType: bool

    queues: List['Queue'] = Relationship(back_populates="queue_owner", link_model=Queue)

    #fk_terms: Optional[int] = Field(default=None, foreign_key="terms.id")
