from uuid import UUID

from pydantic import BaseModel
from sqlmodel import Field

from app.common.base.base_entity import BaseUUIDModel
from app.domain.owner_management.models.owner import Role


class CreateOwnerRequest(BaseModel):
    id: UUID
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=100)
    role: Role.Owner

