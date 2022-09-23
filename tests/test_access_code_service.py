import logging
from datetime import datetime
from typing import Optional
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from app.business.queue_management.models.access import NextCodeCto, RemainingCodes
from app.business.queue_management.services.access import AccessCodeService, parse_to_dto
from app.domain.queue_management.models import AccessCode
from app.common.utils import get_current_time, get_current_date
from app.business.queue_management.models.queue import QueueDto
from app.business.queue_management.services.queue import QueueService
from app.domain.queue_management.models.access_code import Status
from app.domain.queue_management.repositories.access_code import AccessCodeSQLRepository

logger = logging.getLogger(__name__)


def get_queue_dto() -> QueueDto:
    queue = QueueDto(
        id=1,
        modificationCounter=0,
        minAttentionTime=12000,
        started=False,
        createdDate=get_current_date()
    )
    return queue


def get_access_code(status: Status, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> AccessCode:
    access_code = AccessCode(
        id="3fecca55f2424ec68680e0d6961f9d22",
        code="Code1",
        modification_counter=0,
        created_time="2022-9-22 18:17:31.637563",
        start_time=start_time,
        end_time=end_time,
        status=status,
        fk_queue=1,
        fk_visitor="291d3153817c48e0947708ea5bac4783"
    )
    return access_code


def get_next_code_dto(access_code: Optional[AccessCode], remaining_codes: int) -> NextCodeCto:
    next_ticket = NextCodeCto(
        accessCode=parse_to_dto(access_code),
        remainingCodes=RemainingCodes(
            remainingCodes=remaining_codes
        )
    )
    return next_ticket


class AccessCodeServiceTests(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Mocks
        self.mock_access_repo = MagicMock(AccessCodeSQLRepository)
        self.mock_queue_service = MagicMock(QueueService)

        # AccessCodeService
        self.access_code_service = AccessCodeService(
            self.mock_access_repo,
            self.mock_queue_service
        )

    async def test_get_current_ticket_number_is_none(self):
        self.mock_queue_service.get_todays_queue.return_value = get_queue_dto()
        self.mock_access_repo.get_by_queue_status_attending.return_value = None

        # Call to be tested
        response = await self.access_code_service.get_current_ticket_number()

        assert response is None

    async def test_get_current_ticket_number_visitor_is_attending(self):
        self.mock_queue_service.get_todays_queue.return_value = get_queue_dto()
        access_code = get_access_code(Status.Attending)
        self.mock_access_repo.get_by_queue_status_attending.return_value = access_code

        # Call to be tested
        response = await self.access_code_service.get_current_ticket_number()

        assert response == parse_to_dto(access_code)

    async def test_get_remaining_codes_is_called_and_return_zero_values(self):
        self.mock_access_repo.get_remaining_codes.return_value = 0
        # Call to be tested
        returned = await self.access_code_service.get_remaining_codes()
        # Asserts
        assert returned == 0
        self.mock_access_repo.get_remaining_codes.assert_called()

    async def test_get_remaining_codes_is_called_and_return_values(self):
        self.mock_access_repo.get_remaining_codes.return_value = 1
        # Call to be tested
        returned = await self.access_code_service.get_remaining_codes()
        # Asserts
        assert returned >= 0
        self.mock_access_repo.get_remaining_codes.assert_called()

    async def test_parsing_entity_to_dto_when_entity_exists(self):
        access_code = get_access_code(Status.Attending)
        dto = parse_to_dto(access_code)
        assert access_code.id == dto.id
        assert access_code.code == dto.code
        assert access_code.modification_counter == dto.modificationCounter
        assert access_code.created_time == dto.createdDate
        assert access_code.start_time == dto.starTime
        assert access_code.end_time == dto.endTime
        assert access_code.fk_queue == dto.queueId
        assert access_code.fk_visitor == dto.uuid
        assert access_code.status == dto.status

    async def test_parsing_entity_to_dto_when_entity_none(self):
        access_code = None
        dto = parse_to_dto(access_code)
        assert dto is None

    async def test_get_next_ticket_number_when_is_none(self):
        self.mock_queue_service.get_todays_queue.return_value = get_queue_dto()
        self.mock_access_repo.get_by_queue_status_attending.return_value = get_access_code(Status.Attending)
        self.mock_access_repo.get_by_queue_first_waiting.return_value = None
        self.mock_access_repo.get_remaining_codes.return_value = 0

        # Call to be tested
        response = await self.access_code_service.get_next_ticket_number()
        self.mock_access_repo.save.assert_called()
        assert response == get_next_code_dto(None, 0)

    async def test_get_next_ticket_number_when_waiting_is_none(self):
        self.mock_queue_service.get_todays_queue.return_value = get_queue_dto()
        self.mock_access_repo.get_by_queue_status_attending.return_value = get_access_code(Status.Attending)
        self.mock_access_repo.get_by_queue_first_waiting.return_value = None
        self.mock_access_repo.get_remaining_codes.return_value = 0

        # Call to be tested
        response = await self.access_code_service.get_next_ticket_number()
        self.mock_access_repo.save.assert_called()
        assert response == get_next_code_dto(None, 0)

    async def test_get_next_ticket_number_when_attending_is_none(self):
        self.mock_queue_service.get_todays_queue.return_value = get_queue_dto()
        self.mock_access_repo.get_by_queue_status_attending.return_value = None
        self.mock_access_repo.get_by_queue_first_waiting.return_value = None
        self.mock_access_repo.get_remaining_codes.return_value = 0

        # Call to be tested
        response = await self.access_code_service.get_next_ticket_number()
        self.mock_access_repo.save.assert_not_called()
        assert response == get_next_code_dto(None, 0)

    async def test_get_next_ticket_number_when_waiting(self):
        self.mock_queue_service.get_todays_queue.return_value = get_queue_dto()
        self.mock_access_repo.get_by_queue_status_attending.return_value = get_access_code(Status.Attending)
        self.mock_access_repo.get_by_queue_first_waiting.return_value = get_access_code(Status.Waiting)
        self.mock_access_repo.get_remaining_codes.return_value = 1

        # Call to be tested
        response = await self.access_code_service.get_next_ticket_number()
        print(response)
        self.mock_access_repo.save.assert_called()
        assert response == get_next_code_dto(get_access_code(Status.Attending, start_time=response.accessCode.starTime), 1)

    async def test_get_access_code_if_not_exist_in_the_queue(self):
        # create a figurate uuid
        uid = "73b74c82-219d-4cd7-b939-6623fc2fae57"
        today_queue_mock = await self.mock_queue_service.get_todays_queue()

        # Call to be tested
        result = await self.mock_access_repo.get_access_code(today_queue_mock.id, uid)
        response = await self.mock_access_repo.get_last_access_code(today_queue_mock.uid)
        assert response

    async def test_get_last_access_code_should_be_a_value(self):
        today_queue_mock = await self.mock_queue_service.get_todays_queue()
        last_access_code = await self.mock_access_repo.get_last_access_code(today_queue_mock.id)
        assert last_access_code

