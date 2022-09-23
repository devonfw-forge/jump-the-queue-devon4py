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

    async def test_get_or_create_visitor_when_return_an_exception(self):
        self.mock_visitor_repo.create_visitor.return_value = Visitor(
            id='3fa85f64-5717-4562-b3fc-2c963f66afa6'
        )

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
        response = await self.visitor_service.get_or_create_visitor(uid='3fa85f64-5717-4562-b3fc-2c963f66afa6')
        self.mock_visitor_repo.create_visitor.assert_called()
        assert str(response.id) == '3fa85f64-5717-4562-b3fc-2c963f66afa6'

    async def test_get_or_create_visitor_when_return_visitor_exists(self):
        def mocking_create_visitor(uid: str):
            if uid == "test-visitor":
                return test_entity
            else:
                raise NotFoundException

        test_entity = Visitor(
            id='test-visitor'
        )
        self.mock_visitor_repo.side_effect = mocking_create_visitor
        # Call to be tested
        response = await self.visitor_service.get_or_create_visitor(uid='test-visitor')
        self.mock_visitor_repo.create_visitor.assert_not_called()
        assert response.id == test_entity.id
