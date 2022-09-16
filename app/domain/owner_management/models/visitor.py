from typing import List

from sqlmodel import Relationship

from app.common.base.base_entity import *


class Visitor(SQLModel, table=True):
    id: uuid_pkg.UUID = Field(
        default_factory=new_uuid,
        primary_key=True,
        index=True,
        nullable=False,
    )


    #visitor: List['Visitor'] = Relationship(back_populates="access_code")

