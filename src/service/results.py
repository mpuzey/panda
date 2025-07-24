from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, Any

class ResponseType(Enum):
    SUCCESS = 'success'
    NOT_FOUND = 'not_found'
    VALIDATION_ERROR = 'validation_error'
    DATABASE_ERROR = 'database_error'
    BUSINESS_ERROR = 'business_error'


@dataclass
class ServiceResponse:
    response_type: ResponseType
    data: Optional[Any] = None
    errors: Optional[List[str]] = None
    message: Optional[str] = None