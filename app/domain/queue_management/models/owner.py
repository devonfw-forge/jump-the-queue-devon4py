from enum import Enum
from app.common.base.base_entity import BaseUUIDModel


class Role(str, Enum):
    Owner = 'OWNER'
    Employee = 'EMPLOYEE'


class Owner(BaseUUIDModel, table=True):
    username: str
    password: str
    role: Role
