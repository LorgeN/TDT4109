from chattebot import *


class FixedQuestion(Question):
    def __init__(self, data: UserData, question: str):
        self.data = data
        self.question = question

    def get_sentence(self, responses: UserResponses) -> str:
        if responses.has_response(UserData.NAME):
            return f"{self.question}, {responses.get_response(UserData.NAME)}?"
        return f"{self.question}?"

    def get_data_type(self) -> UserData:
        return self.data

    def can_use(self, responses: UserResponses) -> bool:
        return not responses.has_response(self.data)


class OpinionQuestion(Response):
    def __init__(self, depend: UserData, question: str):
        self.depend = depend
        self.question = question

    def get_sentence(self, responses: UserResponses) -> str:
        return f"{self.question} {responses.get_response(self.depend).lower()}?"

    def can_use(self, responses: UserResponses) -> bool:
        return responses.has_response(self.depend)


NAME_QUESTION = FixedQuestion(UserData.NAME, "Hva heter du?")
QUESTIONS = [
    # Questions for fixed data
    FixedQuestion(UserData.AGE, "Hvor gammel er du"),
    FixedQuestion(UserData.MOOD, "Hvordan står det til"),
    FixedQuestion(UserData.MOOD, "Hvordan går det"),
    FixedQuestion(UserData.LOCATION, "Hvor er du fra"),
    FixedQuestion(UserData.LOCATION, "Hvor er du født"),
    FixedQuestion(UserData.ACTIVITY, "Hva gjør du på"),
    FixedQuestion(UserData.ACTIVITY, "Hva gjør du"),
    FixedQuestion(UserData.ACTIVITY, "Hva gjør du akkurat nå"),
    FixedQuestion(UserData.FUTURE, "Hva tenker du om fremtiden"),
    FixedQuestion(UserData.FUTURE, "Har du noen tanker om fremtiden"),

    # Questions regarding opinions on previous answers
    OpinionQuestion(UserData.AGE, "Gleder du deg til å bli ett år eldre, nå som du er"),
    OpinionQuestion(UserData.LOCATION, "Hvorden er det å være i fra"),
    OpinionQuestion(UserData.ACTIVITY, "Har du det gøy når du")
]
