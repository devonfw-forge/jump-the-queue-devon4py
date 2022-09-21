from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock
from app.business.queue_management.services.queue import QueueService, parse_to_dto
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

    async def test_get_todays_queue_is_none_should_create_it(self):
        self.mock_queue_repo.get_today_queue.return_value = None
        self.mock_queue_repo.create_queue.return_value = Queue(id=1)

        # Call to be tested
        await self.queue_service.get_todays_queue()

        self.mock_queue_repo.create_queue.assert_called()

    async def test_get_todays_queue_is_not_none_should_return_it(self):
        self.mock_queue_repo.get_today_queue.return_value = Queue(id=1)

        # Call to be tested
        await self.queue_service.get_todays_queue()

        self.mock_queue_repo.create_queue.assert_not_called()

    async def test_parsing_entity_to_dto(self):
        queue = Queue(id=1)
        dto = parse_to_dto(queue)
        assert queue.id == dto.id
        assert queue.started == dto.started
        assert queue.modificationCounter == dto.modificationCounter
        assert queue.created_date == dto.createdDate
        assert queue.min_attention_time == dto.minAttentionTime

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
