from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock
from app.business.queue_management.services.visitor import VisitorService
from app.common.exceptions.http import NotFoundException
from app.domain.queue_management.models import Visitor
from app.domain.queue_management.repositories.visitor import VisitorSQLRepository


class VisitorServiceTests(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Mocks
        self.mock_visitor_repo = MagicMock(VisitorSQLRepository)

        # VisitorService
        self.visitor_service = VisitorService(
            self.mock_visitor_repo
        )

    async def test_get_or_create_visitor_when_return_an_exception_or_not(self):
        def mocking_create_visitor(uid: str):
            if uid == "test-visitor":
                return test_entity
            else:
                raise NotFoundException

        test_entity = Visitor(
            id='test-visitor'
        )
        self.mock_visitor_repo.get.side_effect = mocking_create_visitor
        # Call to be tested
        ex = False
        try:
            await self.mock_visitor_repo.get(test_entity.id)
        except NotFoundException:
            ex = True
            self.mock_visitor_repo.create_visitor.assert_called_with(test_entity.id)
        assert ex == False
        try:
            await self.mock_visitor_repo.get(test_entity.id)
        except NotFoundException:
            ex = True
            # Asserts
            assert ex == True
