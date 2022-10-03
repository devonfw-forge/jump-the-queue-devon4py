import logging
from datetime import datetime
from typing import Optional
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from app.business.queue_management.models.access import NextCodeCto, RemainingCodes
from app.business.queue_management.services.access import AccessCodeService, parse_to_dto, parse_time_response
from app.business.queue_management.services.visitor import VisitorService
from app.domain.queue_management.models import AccessCode, Visitor
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
        minAttentionTime=120000,
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
        self.mock_visitor_service = MagicMock(VisitorService)

        # AccessCodeService
        self.access_code_service = AccessCodeService(
            self.mock_access_repo,
            self.mock_queue_service,
            self.mock_visitor_service
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
        assert int(access_code.created_time.timestamp()) == dto.createdDate
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
        self.mock_access_repo.save.assert_called()
        assert response == get_next_code_dto(get_access_code(Status.Attending, start_time=response.accessCode.starTime), 1)


    async def test_get_access_code_if_exist_in_the_queue(self):
        # create a figurate uuid
        self.mock_queue_service.get_todays_queue.return_value = get_queue_dto()
        access_code = get_access_code(status=Status.Waiting)
        self.mock_access_repo.get_access_code.return_value = access_code

        # Call to be tested
        response = await self.access_code_service.get_access_code(access_code.fk_visitor)
        self.mock_access_repo.get_last_access_code.assert_not_called()
        self.mock_visitor_service.get_or_create_visitor.assert_not_called()
        self.mock_access_repo.create_code.assert_not_called()
        assert response == parse_to_dto(access_code)

    async def test_get_access_code_if_first_in_the_queue(self):
        # create a figurate uuid
        access_code = get_access_code(status=Status.Waiting)
        access_code.code = 'Q001'
        self.mock_queue_service.get_todays_queue.return_value = get_queue_dto()
        self.mock_access_repo.get_access_code.return_value = None
        self.mock_access_repo.get_last_access_code.return_value = None
        self.mock_visitor_service.get_or_create_visitor.return_value = Visitor(id=access_code.fk_visitor)
        self.mock_access_repo.create_code.return_value = access_code

        # Call to be tested
        response = await self.access_code_service.get_access_code(access_code.fk_visitor)
        assert response == parse_to_dto(access_code)

    async def test_get_access_code_if_second_in_the_queue(self):
        # create a figurate uuid
        access_code_1 = get_access_code(status=Status.Waiting)
        access_code_1.code = 'Q001'
        access_code_2 = get_access_code(status=Status.Waiting)
        access_code_2.code = 'Q002'
        self.mock_queue_service.get_todays_queue.return_value = get_queue_dto()
        self.mock_access_repo.get_access_code.return_value = None
        self.mock_access_repo.get_last_access_code.return_value = access_code_1
        self.mock_visitor_service.get_or_create_visitor.return_value = Visitor(id=access_code_2.fk_visitor)
        self.mock_access_repo.create_code.return_value = access_code_2

        # Call to be tested
        response = await self.access_code_service.get_access_code(access_code_2.fk_visitor)
        assert response == parse_to_dto(access_code_2)

    async def test_get_access_code_if_last_in_the_queue(self):
        # create a figurate uuid
        access_code_1 = get_access_code(status=Status.Waiting)
        access_code_1.code = 'Q999'
        access_code_2 = get_access_code(status=Status.Waiting)
        access_code_2.code = 'Q001'
        self.mock_queue_service.get_todays_queue.return_value = get_queue_dto()
        self.mock_access_repo.get_access_code.return_value = None
        self.mock_access_repo.get_last_access_code.return_value = access_code_1
        self.mock_visitor_service.get_or_create_visitor.return_value = Visitor(id=access_code_2.fk_visitor)
        self.mock_access_repo.create_code.return_value = access_code_2

        # Call to be tested
        response = await self.access_code_service.get_access_code(access_code_2.fk_visitor)
        assert response == parse_to_dto(access_code_2)

    async def test_get_last_access_code_should_be_a_value(self):
        today_queue_mock = await self.mock_queue_service.get_todays_queue()
        last_access_code = await self.mock_access_repo.get_last_access_code(today_queue_mock.id)
        assert last_access_code

    async def test_get_estimated_time_two_waiting_customers(self):
        self.mock_queue_service.get_todays_queue.return_value = get_queue_dto()
        self.mock_access_repo.get_visitors_count.return_value = ['Q006', 'Q007']
        self.mock_access_repo.get_access_code_attended.return_value = [(20, 5), (15, 10)]

        result = await self.access_code_service.get_estimated_time(parse_to_dto(get_access_code(Status.Waiting)))
        assert result == parse_time_response(360000)

    async def test_get_estimated_time_non_waiting(self):
        self.mock_queue_service.get_todays_queue.return_value = get_queue_dto()
        self.mock_access_repo.get_visitors_count.return_value = []
        self.mock_access_repo.get_access_code_attended.return_value = [(200000, 50000), (250000, 100000)]

        result = await self.access_code_service.get_estimated_time(parse_to_dto(get_access_code(Status.Waiting)))
        assert result == parse_time_response(300000)

    async def test_get_estimated_time_non_waiting(self):
        self.mock_queue_service.get_todays_queue.return_value = get_queue_dto()
        self.mock_access_repo.get_visitors_count.return_value = ['Q006', 'Q007']
        self.mock_access_repo.get_access_code_attended.return_value = []

        result = await self.access_code_service.get_estimated_time(parse_to_dto(get_access_code(Status.Waiting)))
        assert result == parse_time_response(360000)

    async def test_leave_queue(self):
        self.mock_queue_service.get_todays_queue.return_value = get_queue_dto()
        self.mock_access_repo.get_access_code.return_value = get_access_code(Status.Waiting)

        response = await self.access_code_service.leave_queue(get_access_code(Status.Waiting).fk_visitor)
        self.mock_access_repo.save.assert_called()
        response = get_access_code(Status.Skipped)
