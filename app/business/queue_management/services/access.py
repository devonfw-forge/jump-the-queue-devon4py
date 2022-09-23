import logging
import uuid
from fastapi import Depends
from typing import Optional

from app.business.queue_management.services.queue import QueueService
from app.business.queue_management.services.visitor import VisitorService
from app.domain.queue_management.models import AccessCode
from app.domain.queue_management.models.access_code import Status
from app.domain.queue_management.repositories.access_code import AccessCodeSQLRepository
from app.business.queue_management.models.access import AccessCodeDto, NextCodeCto, RemainingCodes
from app.common.utils import get_current_time

logger = logging.getLogger(__name__)


def parse_to_dto(access_code_entity: AccessCode) -> Optional[AccessCodeDto]:
    access_code = None
    if access_code_entity:
        access_code = AccessCodeDto(
            id=access_code_entity.id,
            modificationCounter=access_code_entity.modification_counter,
            code=access_code_entity.code,
            uuid=access_code_entity.fk_visitor,
            createdDate=access_code_entity.created_time,
            starTime=access_code_entity.start_time,
            endTime=access_code_entity.end_time,
            status=access_code_entity.status,
            queueId=access_code_entity.fk_queue
        )
    return access_code


class AccessCodeService:

    def __init__(self, repository: AccessCodeSQLRepository = Depends(AccessCodeSQLRepository),
                 queue_service: QueueService = Depends(QueueService), visitor_service: VisitorService = Depends(VisitorService)):
        self.access_code_repo = repository
        self.queue_service = queue_service
        self._visitor_service = visitor_service

    async def get_current_ticket_number(self) -> Optional[AccessCodeDto]:
        today_queue = await self.queue_service.get_todays_queue()
        access_code = await self.access_code_repo.get_by_queue_status_attending(today_queue.id)
        current_ticket = parse_to_dto(access_code)

        return current_ticket

    async def get_next_ticket_number(self) -> Optional[NextCodeCto]:
        today_queue = await self.queue_service.get_todays_queue()
        current_access_code = await self.access_code_repo.get_by_queue_status_attending(today_queue.id)
        if current_access_code:
            current_access_code.status = Status.Attended
            current_access_code.end_time = get_current_time()
            await self.access_code_repo.save(model=current_access_code)
        next_access_code = await self.access_code_repo.get_by_queue_first_waiting(today_queue.id)
        if next_access_code:
            next_access_code.status = Status.Attending
            next_access_code.start_time = get_current_time()
            await self.access_code_repo.save(model=next_access_code)
        next_ticket: NextCodeCto = NextCodeCto(
            accessCode=parse_to_dto(next_access_code),
            remainingCodes=RemainingCodes(
                remainingCodes=await self.access_code_repo.get_remaining_codes()
            )
        )

        return next_ticket

    async def get_access_code(self, uid):
        """
        The function gets the access code for today's current queue and the uuid provided by the front end application.
        Retrieving the last access code if it exists and if it doesn't create it.
        Params: Type: UUID
        Returns: Dto AccessCode.
        """
        # Recovering the current queue
        today_queue = await self.queue_service.get_todays_queue()
        # Extracting if the access code exist
        access_code = await self.access_code_repo.get_access_code(today_queue.id, uid)
        # Comparing if the result is empty (return uuid or not) and if it doesn't exist create it
        if not access_code:
            last_access_code = await self.access_code_repo.get_last_access_code(today_queue.id)
            if not last_access_code:
                new_access_code = 'Q001'
                logger.info(new_access_code)
            else:
                last_code_raw = int(last_access_code.code[1:], 10)
                if last_code_raw > 999:
                    next_code_raw = 1
                else:
                    next_code_raw = last_code_raw + 1
                new_access_code = last_access_code.code[0] + '{0:0>3}'.format(next_code_raw)
                # If Q1000 reset to Q001
            visitor = await self._visitor_service.get_or_create_visitor(uid=uid)
            logger.info(new_access_code)
            access_code = await self.access_code_repo.create_code(queue_id=today_queue.id, visitor_id=visitor.id, new_access_code=new_access_code)

        return parse_to_dto(access_code)

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

