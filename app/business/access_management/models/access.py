from enum import Enum

from pydantic import BaseModel

from app.domain.access_management.models import AccessCode


class CodeRequest(BaseModel):
    pass


class AccessCodeResponse(BaseModel):
    # recogela respuesta de la BD???
    pass


class NextCodeCto(BaseModel):
    pass


class UuidResponse(BaseModel):
    pass


class EstimatedTimeResponse(BaseModel):
    pass


class EstimatedCodeResponse(BaseModel):
    pass





class RemainingCodes:
    remainingCodes: int



