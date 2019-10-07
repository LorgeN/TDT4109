from abc import ABC, abstractmethod
from enum import Enum
from random import shuffle


# Various information we may access to generate more natural questions later
class UserData(Enum):
    NAME = 0
    AGE = 1
    MOOD = 2
    ACTIVITY = 3
    LOCATION = 4
    FUTURE = 5


class UserResponses:
    def __init__(self):
        self.responses = [None for data in UserData]
        self.raw_responses = []

    def has_response(self, data: UserData) -> bool:
        return not self.responses[data.value] is None

    def get_response(self, data: UserData):
        return self.responses[data.value]

    def get_last_response(self) -> str:
        return self.raw_responses[-1]

    def get_raw_responses(self) -> list:
        return self.raw_responses

    def take_input(self, response) -> bool:
        print(response.get_sentence(self))

        raw_in = input(">")
        if raw_in == "hade":
            return False

        self.raw_responses.append(raw_in)

        # Set response if this is a question for a specific data type
        if isinstance(response, Question):
            self.responses[response.get_data_type().value] = raw_in

        return True


class Response(ABC):
    @abstractmethod
    def get_sentence(self, responses: UserResponses) -> str:
        pass

    def can_use(self, responses: UserResponses) -> bool:
        return True


class Question(Response):
    @abstractmethod
    def get_data_type(self) -> UserData:
        pass


def select_response(available_responses: list, user_responses: UserResponses):
    shuffle(available_responses)
    for response in available_responses:
        if response.can_use(user_responses):
            return response
    return None
