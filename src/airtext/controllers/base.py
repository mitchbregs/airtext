import re
from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel

from airtext.api import AirtextAPI


class Request:
    pass


class RequestData(BaseModel):
    to_number: Optional[str]
    from_number: Optional[str]
    body: Optional[str]
    media_url: Optional[str]


class Controller(ABC):
    def __init__(self, request: Request):
        self.request = request
        self.api = AirtextAPI()

    @abstractmethod
    def dispatch_request(self):
        pass
