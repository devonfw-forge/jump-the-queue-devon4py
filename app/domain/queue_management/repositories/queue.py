from fastapi import Depends
from sqlmodel import select

from app.common.base.base_repository import BaseSQLRepository
from app.common.exceptions.http import DevonHttpException
from app.common.infra.sql_adaptors import AsyncSession, get_async_session
from app.common.utils import get_current_date
from app.domain.queue_management.models import Queue


class QueueSQLRepository(BaseSQLRepository[Queue]):
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        super().__init__(Queue, session)

    async def get_today_queue(self):
        queue = await self.session.exec(select(Queue).where(Queue.created_date == get_current_date()))
        return queue.one_or_none()

    async def create_queue(self) -> Queue:
        queue = Queue()
        await self.add(model=queue)
        return queue

    async def update_queue(self):
        current_queue = await self.get_today_queue()
        current_queue.started = True
        current_queue.modificationCounter = 0
        await self.add(model=current_queue)
        return current_queue

