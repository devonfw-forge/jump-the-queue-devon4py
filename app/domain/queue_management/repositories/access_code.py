import logging
from uuid import UUID
from fastapi import Depends
from sqlalchemy import func, desc
from sqlmodel import select
from typing import Optional

from app.common.base.base_repository import BaseSQLRepository
from app.domain.queue_management.models.access_code import AccessCode
from app.common.infra.sql_adaptors import AsyncSession, get_async_session
from app.domain.queue_management.models.access_code import Status

logger = logging.getLogger(__name__)


class AccessCodeSQLRepository(BaseSQLRepository[AccessCode]):
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        super().__init__(AccessCode, session)

    async def get_by_queue_status_attending(self, queue_id: UUID) -> Optional[AccessCode]:
        access_code = await self.session.exec(select(AccessCode).where(AccessCode.fk_queue == queue_id, AccessCode.
                                                                       status == Status.Attending))
        return access_code.one_or_none()

    async def get_remaining_codes(self) -> int:
        waiting = await self.session.exec(select([func.count(AccessCode.id)])
                                          .where(AccessCode.status == Status.Waiting))
        return waiting.one()  # Type: ignore

    async def get_by_queue_first_waiting(self, queue_id: UUID) -> Optional[AccessCode]:
        access_code = await self.session.exec(select(AccessCode).where(AccessCode.fk_queue == queue_id, AccessCode.
                                                                       status == Status.Waiting))
        return access_code.first()

    async def save(self, *, model: AccessCode, refresh: bool = True):
        model.modification_counter += 1
        return await super().save(model=model, refresh=refresh)

    async def get_access_code(self, queue_id, uuid):
        uuid = str(uuid)
        access_code = await self.session.exec(
            select(AccessCode).where(AccessCode.fk_queue == queue_id).where(AccessCode.fk_visitor == uuid))
        return access_code.one_or_none()

    async def get_last_access_code(self, queue_id) -> AccessCode:
        last_code = await self.session.exec(select(AccessCode).where(AccessCode.fk_queue == queue_id).order_by(desc(AccessCode.created_time)))
        return last_code.first()

    async def create_code(self, *, queue_id: int, visitor_id: UUID, new_access_code: str) -> AccessCode:
        access = AccessCode(code=new_access_code, fk_queue=queue_id, fk_visitor=visitor_id)
        await self.add(model=access)
        return access




