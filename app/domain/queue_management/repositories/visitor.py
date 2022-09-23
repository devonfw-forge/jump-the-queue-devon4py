from fastapi import Depends
from select import select

from app.common.base.base_entity import BaseUUIDModel
from app.common.base.base_repository import BaseSQLRepository
from app.common.infra.sql_adaptors import AsyncSession, get_async_session
from app.common.utils import get_current_date, get_current_time
from app.domain.queue_management.models import Visitor, Queue, AccessCode


class VisitorSQLRepository(BaseSQLRepository[Visitor]):
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        super().__init__(Visitor, session)

    async def create_visitor(self, uid) -> Visitor:
        """
        Function to create a new visitor
        Args: uid
        Use: method add() from base_repository of common files
        Returns: an object of type entity Visitor
        """
        visitor = Visitor(id=uid)
        await self.add(model=visitor)
        return visitor

