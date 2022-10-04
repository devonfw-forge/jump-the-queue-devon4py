import datetime
import logging
from uuid import UUID

from fastapi import Depends
from typing import Optional
from sse_starlette import ServerSentEvent
from app.business.queue_management.services.queue import QueueService
from app.business.queue_management.services.visitor import VisitorService
from app.common.services.sse import EventPublisher
from app.domain.queue_management.models import AccessCode
from app.domain.queue_management.models.access_code import Status
from app.domain.queue_management.repositories.access_code import AccessCodeSQLRepository
from app.business.queue_management.models.access import AccessCodeDto, NextCodeCto, RemainingCodes, \
    EstimatedTimeResponse, AccessCodeResponse
from app.business.queue_management.models.queue import SseTopic, QueueDto
from app.common.utils import get_current_time

logger = logging.getLogger(__name__)


def response_json(access_code: AccessCodeDto, queue: QueueDto) -> AccessCodeResponse:
    return AccessCodeResponse(
        accessCode=access_code,
        queue=queue
    )


def parse_to_dto(access_code_entity: AccessCode) -> Optional[AccessCodeDto]:
    access_code = None
    if access_code_entity:
        access_code = AccessCodeDto(
            id=access_code_entity.id,
            modificationCounter=access_code_entity.modification_counter,
            code=access_code_entity.code,
            uuid=access_code_entity.fk_visitor,
            createdDate=access_code_entity.created_time.timestamp(),
            starTime=access_code_entity.start_time.timestamp() if access_code_entity.start_time else None,
            endTime=access_code_entity.end_time.timestamp() if access_code_entity.end_time else None,
            status=access_code_entity.status,
            queueId=access_code_entity.fk_queue
        )
    return access_code


def parse_time_response(estimated_attention_time: int) -> EstimatedTimeResponse:
    return EstimatedTimeResponse(
        miliseconds=estimated_attention_time,
        defaultTimeByUserInMs=120000
    )


class AccessCodeService:
    access_event_publisher = EventPublisher()

    def __init__(self, repository: AccessCodeSQLRepository = Depends(AccessCodeSQLRepository),
                 queue_service: QueueService = Depends(QueueService),
                 visitor_service: VisitorService = Depends(VisitorService)):
        self.access_code_repo = repository
        self.queue_service = queue_service
        self._visitor_service = visitor_service

    def add_sse(self) -> ServerSentEvent:
        _, sse = self.access_event_publisher.subscribe()
        return sse

    async def get_current_ticket_number(self) -> Optional[AccessCodeDto]:
        """
        The function gets the access code number of the current customer who is being attended from today's queue.
        Retrieving the current access code if it exists, if not return none.
        Params: None
        Returns: AccessCodeDto | None.
        """
        today_queue = await self.queue_service.get_todays_queue()
        access_code = await self.access_code_repo.get_by_queue_status_attending(today_queue.id)
        current_ticket = parse_to_dto(access_code)

        return current_ticket

    async def get_next_ticket_number(self) -> NextCodeCto:
        """
        The function calls the next access code from today's queue.
        Params: None
        Returns: NextCodeDto
        """
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
            self.access_event_publisher.publish(data=parse_to_dto(next_access_code).json(), topic=SseTopic.CURRENT_CODE_CHANGED)
        else:
            self.access_event_publisher.publish(data=parse_to_dto(next_access_code).json(),
                                                topic=SseTopic.CURRENT_CODE_CHANGED_NULL)
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
                last_code_raw = int(last_access_code.code[1:])
                if last_code_raw >= 999:
                    next_code_raw = 1
                else:
                    next_code_raw = last_code_raw + 1
                new_access_code = last_access_code.code[0] + '{0:0>3}'.format(next_code_raw)

                # If Q1000 reset to Q001
            visitor = await self._visitor_service.get_or_create_visitor(uid=uid)
            logger.info(new_access_code)
            access_code = await self.access_code_repo.create_code(queue_id=today_queue.id, visitor_id=visitor.id,
                                                                  new_access_code=new_access_code)
            # SSE notify
            self.access_event_publisher.publish(data=parse_to_dto(access_code).json(), topic=SseTopic.NEW_CODE_ADDED)
        return response_json(parse_to_dto(access_code), today_queue)

    async def get_estimated_time(self, access_code_request: AccessCodeDto) -> EstimatedTimeResponse:
        """
        The function gets the estimation time that a customer should be wait in the queue before being attended.
        Params: AccessCodeDto
        Returns: EstimatedTimeResponse
        """
        today_queue = await self.queue_service.get_todays_queue()
        # Looking for the total of visitors not attended in the Queue except the uid with status Waiting
        visitors_before_current_client = await self.access_code_repo.get_visitors_count(today_queue.id,
                                                                                        access_code_request.uuid)
        # total of visitors waiting in the queue + the one that is being attended
        nb_non_attented_customers = len(visitors_before_current_client) + 1
        # attention_time: The time between the moment the customer starts to be served and the moment
        # the next customer is called
        attended_customers_times = await self.access_code_repo.get_access_code_attended(today_queue.id)
        attention_time = list(map(lambda x: (x[0] - x[1]).seconds if (x[0] - x[1]).seconds >= today_queue.minAttentionTime else today_queue.minAttentionTime, attended_customers_times))
        # average_attention_time:
        # (The sum of attention_time from the first attended customer until the last attended customer before me) /
        # the number of the no attended customers in queue before me.
        try:
            average_attention_time = sum(attention_time) / len(attention_time)
        except ZeroDivisionError:
            average_attention_time = 120000
        # attention_time: average_attention_time ∗ (nº of no attended customers in queue before me)
        estimated_attention_time = average_attention_time * nb_non_attented_customers

        return parse_time_response(estimated_attention_time)

    async def get_remaining_codes(self) -> int:
        """
        Function get amount of remaining codes (pending/waiting to be called) into de DataBase.
        Params: There is no params.
        Returns: an Integer of number of objects AccessCode.
        """
        # Get amount of remaining codes (pending/waiting to be called)
        codes = await self.access_code_repo.get_remaining_codes()
        return codes

    async def leave_queue(self, visitor_id: UUID) -> AccessCodeDto:
        today_queue = await self.queue_service.get_todays_queue()
        access_code = await self.access_code_repo.get_access_code(today_queue.id, visitor_id)
        access_code.status = Status.Skipped
        await self.access_code_repo.save(access_code)

        return parse_to_dto(access_code)
