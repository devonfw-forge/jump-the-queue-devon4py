from typing import Optional
from fastapi import Depends
from sqlmodel import select

from app.common.base.base_repository import BaseSQLRepository
from app.common.exceptions.http import NotFoundException
from app.common.infra.sql_adaptors import AsyncSession, get_async_session
from app.domain.queue_management.models import Owner


class OwnerSQLRepository(BaseSQLRepository[Owner]):
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        super().__init__(Owner, session)

    async def get_owner(self, username: str, password: str) -> Optional[Owner]:
        owner = await self.session.exec(select(Owner).where(
            Owner.username == username,
            Owner.password == password))
        return owner.one_or_none()
