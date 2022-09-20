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

    async def test_start_queue_when_should_be_closed(self):
        self.mock_queue_repo.update_queue.return_value = Queue(id=1)

        # Call to be tested
        await self.queue_service.start_queue(request=True)

        self.mock_queue_repo.update_queue.assert_called()




