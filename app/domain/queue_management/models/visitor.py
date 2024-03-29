from typing import List

from app.common.base.base_entity import *


class Visitor(SQLModel, table=True):
    id: uuid_pkg.UUID = Field(
        primary_key=True,
        index=True,
        nullable=False,
    )


