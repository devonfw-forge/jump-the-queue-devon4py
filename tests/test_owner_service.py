from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock
from app.business.queue_management.services.owner import OwnerService, parse_to_dto
from app.business.queue_management.models.owner import OwnerRequest, PageableRequest
from app.domain.queue_management.models.owner import Owner, Role
from app.domain.queue_management.repositories.owner import OwnerSQLRepository


def get_owner_request():
    owner_request = OwnerRequest(
        username="user",
        password="password",
        pageable=PageableRequest(
            pageNumber=0,
            pageSize=1,
            sort=[{
                "direction": "ASC",
                "property": "username",
                "ignoreCase": False,
                "nullHandling": "NATIVE",
                "ascending": True
            }]
        )
    )
    return owner_request


def get_owner():
    owner = Owner(
        username="user",
        password="password",
        role=Role.Owner
    )
    return owner


class OwnerServiceTests(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Mocks
        self.mock_owner_repo = MagicMock(OwnerSQLRepository)
        # VisitorService
        self.owner_service = OwnerService(
            self.mock_owner_repo
        )

    async def test_get_owner_when_return_none(self):
        self.mock_owner_repo.get_owner.return_value = None
        # Call to be tested
        response = await self.owner_service.get_owner(get_owner_request())
        assert response is None

    async def test_get_owner_when_return_owner(self):
        owner = get_owner()
        self.mock_owner_repo.get_owner.return_value = owner
        # Call to be tested
        response = await self.owner_service.get_owner(get_owner_request())
        assert response == parse_to_dto(owner)

