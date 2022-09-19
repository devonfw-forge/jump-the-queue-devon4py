import logging
from fastapi import APIRouter
from app.business.access_management.services.access import *
router = APIRouter(prefix="/access")