import logging

from fastapi import Depends
from app.business.access_management.models.access import AccessCodeDto
from app.domain.access_management.models import AccessCode
from app.domain.access_management.repositories.access_code import AccessCodeSQLRepository



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

#print(new_tickets)



class AccessCodeService:

    def __init__(self, repository: AccessCodeSQLRepository = Depends(AccessCodeSQLRepository)):
        self.access_code_repo = repository


    # REQUEST
    async def get_ticket_number(self, request):
        pass
        # if request.method == 'POST':
        #     todaysQueue = get_or_create_today_queue_serializer()
        #     currentCode = AccessCode.uuid.filter(queueId=todaysQueue.data['id'],
        #                                             status=AccessCodeStatus.ATTENDING.value).first()
        #     currentCodeSerializer = AccessCodeSerializer(currentCode)
        #     return JsonResponse(currentCodeSerializer.data, status=200)

    async def get_next_ticket_number(self, request):
        pass

    async def get_uuid(self, request):
        pass

    async def get_estimated_time(self, request):
        pass

    async def get_remaining_codes(self) -> int:
        # Get amount of remaining codes (pending/waiting to be called)
        codes = await self.access_code_repo.get_remaining_codes()

        return codes


