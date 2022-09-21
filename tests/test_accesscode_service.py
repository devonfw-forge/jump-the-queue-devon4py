import logging
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock
from app.business.access_management.services.access import AccessCodeService
from app.domain.access_management.repositories.access_code import AccessCodeSQLRepository

logger = logging.getLogger(__name__)


class AccessCodeServiceTests(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Mocks
        self.mock_access_repo = MagicMock(AccessCodeSQLRepository)

        # QueueService
        self.access_service = AccessCodeService(
            self.mock_access_repo
        )

    async def test_get_remaining_codes_is_called_and_return_zero_values(self):
        self.mock_access_repo.get_remaining_codes.return_value = 0
        # Call to be tested
        returned = await self.access_service.get_remaining_codes()
        # Asserts
        assert returned == 0
        self.mock_access_repo.get_remaining_codes.assert_called()

    async def test_get_remaining_codes_is_called_and_return_values(self):
        self.mock_access_repo.get_remaining_codes.return_value = 1
        # Call to be tested
        returned = await self.access_service.get_remaining_codes()
        # Asserts
        assert returned >= 0
        self.mock_access_repo.get_remaining_codes.assert_called()