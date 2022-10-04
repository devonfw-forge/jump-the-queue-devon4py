from typing import List
from uuid import UUID

from pydantic import BaseModel
from sqlmodel import Field

from app.domain.queue_management.models.owner import Role


class CreateOwnerRequest(BaseModel):
    id: UUID
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=100)
    role: Role.Owner


class PageableRequest(BaseModel):
    pageNumber: int
    pageSize: int
    sort: List[dict]


class OwnerRequest(BaseModel):
    username: str
    password: str
    pageable: PageableRequest


class OwnerDto(BaseModel):
    id: UUID
    modificationCounter: int
    username: str
    password: str
    userType: bool
