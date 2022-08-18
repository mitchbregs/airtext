from abc import ABC, abstractmethod
from airtext.api import AirtextAPI
from airtext.controllers.request import MessageRequest


class Controller(ABC):
    def __init__(self, request: MessageRequest):
        self.request = request
        self.api = AirtextAPI()

    @abstractmethod
    def dispatch_request(self):
        pass
