import logging
from fastapi import APIRouter, Depends
from app.business.access_management.services.access import *
from app.business.queue_management.services.queue import QueueService

router = APIRouter(prefix="/owner")