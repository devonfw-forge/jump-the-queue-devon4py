from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock
from app.business.queue_management.services.queue import QueueService, parse_to_dto
from app.domain.queue_management.repositories.queue import QueueSQLRepository


class QueueServiceTests(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Mocks
        self.mock_queue_repo = MagicMock(QueueSQLRepository)

        # QueueService
        self.queue_service = QueueService(
            self.mock_queue_repo
        )

    async def test_get_todays_queue_is_none(self):

        queue_to_return = self.mock_queue_repo.get_today_queue.return_value

        # Call to be tested
        queue_return = self.queue_service.get_todays_queue

        if queue_to_return is not None:
            print("comprobado 1")
            assert self.mock_queue_repo.create_queue.called == False
        # Assert 1 (if is None, create it)
        queue_to_return = None
        if queue_to_return is None:
            print("comprobado 2")
            assert await self.mock_queue_repo.create_queue()

        # Assert 2 (If is not None, don`t call to create it)



        # Assert 3

        # result = self.queue_service.get_todays_queue
        # assert parse_to_dto(result)
        #result = await self.queue_service.get_todays_queue()
       # print(type(result))

        # Assserts
        #assert parse_to_dto(result)