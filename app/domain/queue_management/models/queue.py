
from typing import List, Optional

from sqlmodel import Relationship, SQLModel, Field
import uuid as uuid_pkg
from app.common.base.base_entity import new_uuid
from app.domain.queue_management.models.access_code import AccessCode
from app.domain.queue_management.models.visitor import Visitor


# from app.common.base.base_entity import *
# from app.domain.queue_management.models.access_code import AccessCode
# from app.domain.queue_management.models.terms import Terms
#from app.domain.queue_management.models.user import *
from app.domain.queue_management.models.visitor import Visitor


class Queue(SQLModel, table=True):
    id: uuid_pkg.UUID = Field(
        default_factory=new_uuid,
        primary_key=True,
        index=True,
        nullable=False
    )
    name: str
    logo: str
    description: str
    accessLink: str
    minAttentionTime: int
    openTime: str
    closeTime: str

   #access_id: str = Field(default=None, foreign_key="access-code.id", nullable=True)

    my_access: List[AccessCode] = Relationship(back_populates="queue")
    #book_id: uuid_pkg.UUID = Field(default=None, foreign_key="book.id", nullable=True)
    #user: Optional[User] = Relationship(back_populates="queue")
    #terms: List[Terms] = Relationship(back_populates="queue")

    #visitor: List[Visitor] = Relationship(back_populates="queue")
    #
    # user_client: str = Field(default=None, foreign_key="user.clientId", nullable=True)
    # visitorUID: uuid_pkg.UUID = Field(default=None, foreign_key="queue.id", nullable=True)
# class Team(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str = Field(index=True)
#     headquarters: str
#
#
# class Hero(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str = Field(index=True)
#     secret_name: str
#     age: Optional[int] = Field(default=None, index=True)
#
#     team_id: Optional[int] = Field(default=None, foreign_key="team.id")
