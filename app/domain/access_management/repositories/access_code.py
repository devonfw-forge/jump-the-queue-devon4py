from uuid import UUID
from fastapi import Depends
from sqlmodel import select
from typing import Optional

from app.common.base.base_repository import BaseSQLRepository
from app.domain.access_management.models.access_code import AccessCode
from app.common.infra.sql_adaptors import AsyncSession, get_async_session


class AccessCodeSQLRepository(BaseSQLRepository[AccessCode]):
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        super().__init__(AccessCode, session)

    async def get_by_queue_status_attending(self, queue_id: UUID) -> Optional[AccessCode]:
        access_code = await self.session.exec(select(AccessCode).where(AccessCode.fk_queue == queue_id, AccessCode.
                                                                       status == 'ATTENDING'))
        return access_code.one_or_none()
