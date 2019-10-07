from chattebot import Response, UserResponses, UserData


class FollowUpQuestion(Response):
    def __init__(self, base: str):
        self.base = base

    def get_sentence(self, responses: UserResponses) -> str:
        if responses.has_response(UserData.NAME):
            return f"{self.base} \"{responses.get_last_response().lower()}\", {responses.get_response(UserData.NAME)}?"

        return f"{self.base} \"{responses.get_last_response().lower()}\"?"


FOLLOW_UP_QUESTIONS = [
    FollowUpQuestion("Hvorfor sier du"),
    FollowUpQuestion("Hva mener du med"),
    FollowUpQuestion("Hvor lenge har du sagt"),
    FollowUpQuestion("Hvilke tanker har du om"),
    FollowUpQuestion("Kan du si litt mer om"),
    FollowUpQuestion("Når tenkte du første gang på")
]
