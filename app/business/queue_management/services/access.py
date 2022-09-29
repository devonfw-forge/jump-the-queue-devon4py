import datetime
import logging
from fastapi import Depends
from typing import Optional
from app.business.queue_management.services.queue import QueueService
from app.business.queue_management.services.visitor import VisitorService
from app.common.exceptions.runtime import DevonCustomException
from app.domain.queue_management.models import AccessCode
from app.domain.queue_management.models.access_code import Status
from app.domain.queue_management.repositories.access_code import AccessCodeSQLRepository
from app.business.queue_management.models.access import AccessCodeDto, NextCodeCto, RemainingCodes, AccessCodeStatus, \
    EstimatedTimeResponse
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


def parse_datetime_to_int(current_date: datetime):
    return int(current_date.strftime("%Y%m%d%H%M%S"))


current_date = datetime.datetime.now()
print(type(parse_datetime_to_int(current_date)))


def parse_int_to_datetime(timestamp):
    time = datetime.datetime.fromtimestamp(timestamp)
    return time


timestamp = datetime.datetime.fromtimestamp(1500000000)
print(timestamp.strftime('%Y-%m-%d %H:%M:%S'))


class AccessCodeService:

    def __init__(self, repository: AccessCodeSQLRepository = Depends(AccessCodeSQLRepository),
                 queue_service: QueueService = Depends(QueueService),
                 visitor_service: VisitorService = Depends(VisitorService)):
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
            access_code = await self.access_code_repo.create_code(queue_id=today_queue.id, visitor_id=visitor.id,
                                                                  new_access_code=new_access_code)

        return parse_to_dto(access_code)

    async def get_estimated_time(self):
        """
        Function with the following steps:
        1.- Looking for the total of visitors not attended en the Queue except the uid with status "Waiting" and counting them
        2.- Looking for the first attended before me and looking for the last attended before me
        3.- Calculate the attended time with the visitors attended
        4.- The waiting_time cannot be shorter than a configured minimum waiting_time. If that happens,
             the waiting_time is set to that configured minimum waiting_time.
        Returns: a dictionary in milliseconds of type int

        """

        uid = "3fa85f64-5717-4562-b3fc-2c963f66afa0"
        TIME_PER_VISITOR: int = 120000
        today_queue = await self.queue_service.get_todays_queue()
        # Looking for the total of visitors not attended en the Queue except the uid with status Waiting"

        visitors_before = await self.access_code_repo.get_visitors_count(today_queue.id, uid)
        # Looking for the first attended before me and looking for the last attended before me
        count_visitors_before = 0
        try:
            if visitors_before is not None:
                count_visitors_before = len(visitors_before)


        except Exception as e:
            logger.error(e)

        # The attention_time is calculated as: The time between the moment the customer starts to be served
        # and the moment the next customer is called

        attended_time = await self.access_code_repo.get_attended_time(today_queue.id)
        group_stamp = []
        media_group = []
        counter = 0
        try:
            if attended_time is not None:
                for data in attended_time:
                    group_stamp.append(datetime.datetime.timestamp(data))
                    if counter > 0:
                        minus = group_stamp[counter] - group_stamp[counter - 1]
                        media_group.append(minus)
                    counter += 1
                sum_attended_time = sum(media_group)
                attention_time = int(sum_attended_time)
                # in miliseconds
                attention_time = attention_time * 1000

                # The waiting_time cannot be shorter than a configured minimum waiting_time. If that happens,
                # the waiting_time is set to that configured minimum waiting_time.
                if attention_time < TIME_PER_VISITOR:
                    attention_time = TIME_PER_VISITOR

                estimated_waiting_time = count_visitors_before * attention_time
                timed = TIME_PER_VISITOR
                estimated = {'miliseconds': estimated_waiting_time, 'defaultTimeByUserInMs': timed}

                return estimated
        except DevonCustomException as e:
            logger.error("Any value is None: " + e)

    async def get_remaining_codes(self) -> int:
        """
        Function get amount of remaining codes (pending/waiting to be called) into de DataBase.
        Params: There is no params.
        Returns: an Integer of number of objects AccessCode.
        """
        # Get amount of remaining codes (pending/waiting to be called)
        codes = await self.access_code_repo.get_remaining_codes()
        return codes
