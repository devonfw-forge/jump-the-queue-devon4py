from fastapi import Depends
from app.domain.access_management.repositories.access_code import AccessCodeSQLRepository


class AccessCodeService:

    def __init__(self, repository: AccessCodeSQLRepository = Depends(AccessCodeSQLRepository)):
        self.access_code_repo = repository

    # REQUEST
    async def get_ticket_number(self, request):
        pass

    async def get_next_ticket_number(self, request):
        pass

    async def get_uuid(self, request):
        pass

    async def get_estimated_time(self, request):
        pass

    # Request/Responses
    async def get_remaining_codes(self) -> int:
        """
        Function get amount of remaining codes (pending/waiting to be called) into de DataBase.
        Params: There is no params.
        Returns: an Integer of number of objects AccessCode.
        """
        # Get amount of remaining codes (pending/waiting to be called)
        codes = await self.access_code_repo.get_remaining_codes()
        return codes
