from typing import Optional, TypeVar

from pydantic import BaseModel

T = TypeVar('T')


class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None