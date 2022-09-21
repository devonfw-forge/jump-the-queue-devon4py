import logging
from fastapi import Depends
from sqlalchemy import func
from sqlmodel import select
from app.common.base.base_repository import BaseSQLRepository
from app.common.infra.sql_adaptors import AsyncSession, get_async_session
from app.domain.access_management.models import AccessCode
from app.domain.access_management.models.access_code import Status

logger = logging.getLogger(__name__)

class AccessCodeSQLRepository(BaseSQLRepository[AccessCode]):
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        super().__init__(AccessCode, session)

    async def get_remaining_codes(self) -> int:
        waiting = await self.session.exec(select([func.count(AccessCode.id)])
                                          .where(AccessCode.status == Status.Waiting))
        return waiting.one()  # Type: ignore



