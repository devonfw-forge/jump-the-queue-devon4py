import logging
from fastapi import Depends
from typing import Optional
from app.business.queue_management.services.queue import QueueService
from app.domain.access_management.models import AccessCode
from app.domain.access_management.repositories.access_code import AccessCodeSQLRepository
from app.business.access_management.models.access import AccessCodeDto


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
                 queue_service: QueueService = Depends(QueueService)):
        self.access_code_repo = repository
        self.queue_service = queue_service

    async def get_current_ticket_number(self) -> Optional[AccessCodeDto]:
        today_queue = await self.queue_service.get_todays_queue()
        access_code = await self.access_code_repo.get_by_queue_status_attending(today_queue.id)
        current_ticket = parse_to_dto(access_code)

        return current_ticket

    async def get_next_ticket_number(self, request):
        pass

    async def get_uuid(self, request):
        pass

    async def get_estimated_time(self, request):
        pass

    async def get_remaining_code(self, request):
        pass


# class QueueSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Queue
#         fields = ['id', 'modificationCounter', 'minAttentionTime', 'started', 'createdDate']


def ticket_generator(letter="Q", letter_position='left', init_num=1, max_num=1000):
    try:
        tickets = []
        letter = letter.upper()
        repeat = max_num - 1
        rep_str = str(repeat)
        rep_num = len(rep_str)
        for x in range(init_num, max_num):
            y = str(x)
            if letter_position == 'left':
                my_num = y.zfill(rep_num)
                tickets.append(letter + my_num)

            if letter_position == 'right':
                my_num = y.zfill(rep_num)
                tickets.append(my_num + letter)
        return tickets
    except ValueError:
        print("Not correct type of value at the params")


# list of tickets
new_tickets = ticket_generator()

# print(new_tickets)
