from chattebot import Response, UserData, UserResponses


class Remark(Response):
    def __init__(self, base: str):
        self.base = base

    def get_sentence(self, responses: UserResponses) -> str:
        if responses.has_response(UserData.NAME):
            return f"{self.base}, {responses.get_response(UserData.NAME)}."
        return f"{self.base}."


REMARKS = [
    Remark("Fint du sier det"),
    Remark("Det skjønner jeg godt"),
    Remark("Så dumt da"),
    Remark("Følger meg også sånn"),
    Remark("Blir trist av det du sier"),
    Remark("Så bra"),
    Remark("Så flott"),
    Remark("Du er jammen frekk")
]
