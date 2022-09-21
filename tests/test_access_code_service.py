import logging
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock
from app.business.queue_management.services.access import AccessCodeService, parse_to_dto
from app.common.utils import get_current_time, get_current_date
from app.domain.access_management.models import AccessCode
from app.business.queue_management.models.queue import QueueDto
from app.business.queue_management.services.queue import QueueService
from app.domain.queue_management.repositories.access_code import AccessCodeSQLRepository

logger = logging.getLogger(__name__)


class AccessCodeServiceTests(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Mocks
        self.mock_access_repo = MagicMock(AccessCodeSQLRepository)
        self.mock_queue_service = MagicMock(QueueService)

        # QueueService
        self.access_code_service = AccessCodeService(
            self.mock_access_repo,
            self.mock_queue_service
        )

    async def test_get_current_ticket_number_is_none(self):
        self.mock_queue_service.get_todays_queue.return_value = QueueDto(
            id=1,
            modificationCounter=0,
            minAttentionTime=12000,
            started=False,
            createdDate=get_current_date()
        )
        self.mock_access_repo.get_by_queue_status_attending.return_value = None

        # Call to be tested
        response = await self.access_code_service.get_current_ticket_number()

        assert response is None

    async def test_get_current_ticket_number_visitor_is_attending(self):
        self.mock_queue_service.get_todays_queue.return_value = QueueDto(
            id=1,
            modificationCounter=0,
            minAttentionTime=12000,
            started=False,
            createdDate=get_current_date()
        )
        access_code = AccessCode(
            code="Code1",
            modification_counter=0,
            created_time=get_current_time(),
            status="ATTENDING",
            fk_queue=1,
            fk_visitor="291d3153817c48e0947708ea5bac4783"
        )
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
        access_code = AccessCode(
            code="Code1",
            modification_counter=0,
            created_time=get_current_time(),
            status="ATTENDING",
            fk_queue=1,
            fk_visitor="291d3153817c48e0947708ea5bac4783"
        )
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
