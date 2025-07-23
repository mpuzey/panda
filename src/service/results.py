from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, Any


class ResultType(Enum):
    SUCCESS = "success"
    NOT_FOUND = "not_found"
    VALIDATION_ERROR = "validation_error"
    DATABASE_ERROR = "database_error"


@dataclass
class ServiceResult:
    result_type: ResultType
    data: Optional[Any] = None
    errors: Optional[List[str]] = None
    message: Optional[str] = None 