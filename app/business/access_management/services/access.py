from fastapi import Depends

from app.domain.access_management.models import AccessCode
from app.domain.access_management.repositories.acces_code import AccessCodeSQLRepository


class RemainingCodes:
    remainingCodes: int


class NextCodeCto:
    accessCode: AccessCode
    remainingCodes: RemainingCodes





class AccessCodeService:

    def __init__(self, repository: AccessCodeSQLRepository = Depends(AccessCodeSQLRepository)):
        self.access_code_repo = repository

    async def get_ticket_number(self):
        pass

    async def get_next_ticket_number(self):
        pass

    async def get_uuid(self):
        pass

    async def get_estimated_time(self):
        pass

    async def get_remaining_code(self):
        pass