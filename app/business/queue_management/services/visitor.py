from typing import Optional

from fastapi import Depends

from app.common.exceptions.http import NotFoundException
from app.domain.queue_management.models import Visitor
from app.domain.queue_management.repositories.visitor import VisitorSQLRepository


class VisitorService:

    def __init__(self, repository: VisitorSQLRepository = Depends(VisitorSQLRepository)):
        self.visitor_repo = repository

    async def get_or_create_visitor(self, uid):
        try:
            visitor = await self.visitor_repo.get(uid=uid)
        except NotFoundException:
            visitor = await self.visitor_repo.create_visitor(uid)
        return visitor
