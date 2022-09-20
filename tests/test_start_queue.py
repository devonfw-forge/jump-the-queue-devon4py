from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from app.business.queue_management.services.queue import QueueService
from app.domain.queue_management.models import Queue
from app.domain.queue_management.repositories.queue import QueueSQLRepository


class QueueServiceTests(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Mocks
        self.mock_queue_repo = MagicMock(QueueSQLRepository)

        # QueueService
        self.queue_service = QueueService(
            self.mock_queue_repo
        )

    async def test_start_queue_when_is_closed(self):
        test_queue = Queue(id=1, started=False)
        self.mock_queue_repo.get.return_value = test_queue

        # Call to be tested
        updated_queue = await self.queue_service.start_queue(uid=1)

        self.mock_queue_repo.save.assert_called()
        assert updated_queue.started == True

    async def test_start_queue_when_is_started(self):
        test_queue = Queue(id=1, started=True)
        self.mock_queue_repo.get.return_value = test_queue

        # Call to be tested
        updated_queue = await self.queue_service.start_queue(uid=1)

        self.mock_queue_repo.save.assert_not_called()
        assert updated_queue.started == True



