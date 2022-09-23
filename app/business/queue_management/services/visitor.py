from fastapi import Depends
from app.common.exceptions.http import NotFoundException
from app.domain.queue_management.repositories.visitor import VisitorSQLRepository


class VisitorService:

    def __init__(self, repository: VisitorSQLRepository = Depends(VisitorSQLRepository)):
        self.visitor_repo = repository

    async def get_or_create_visitor(self, uid):
        """
        Function get  or create a visitor
        Args: uid
        Returns: If exist, get a visitor. If not exist create a new visitor
                 with the function create_visitor with the same uid param
        """
        try:
            visitor = await self.visitor_repo.get(uid=uid)
        except NotFoundException:
            visitor = await self.visitor_repo.create_visitor(uid)
        return visitor

