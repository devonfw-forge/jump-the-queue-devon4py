import uuid
from typing import Optional

from sqlmodel import Field

from app.common.base.base_entity import BaseUUIDModel


class AccessCode_Visitor_Link(BaseUUIDModel, table=True):
    visitor_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="visitor.id", primary_key=True
    )
    access_code_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="access_code.id", primary_key=True
    )