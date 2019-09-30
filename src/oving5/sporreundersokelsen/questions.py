from abc import ABC, abstractmethod
from sporreundersokelsen import ResponseTracker, Question


class GenderQuestion(Question):
    def get_question(self, responses: ResponseTracker) -> str:
        return "Hvilket kjønn er du? [f/m]"

    def is_valid_input(self, input_str: str) -> bool:
        lower_case_str = input_str.lower()
        return lower_case_str == "f" or lower_case_str == "m"

    def accept_input(self, input_str: str) -> tuple:
        # boolean value store, male = True, female = False
        return input_str.lower() == "m", True

    def analyze(self, responses: list):
        count_female = 0
        count_male = 0

        for gender in responses:
            # boolean value store, male = True, female = False
            if gender:
                count_male += 1
            else:
                count_female += 1

        print(f"Antall kvinner: {count_female}")
        print(f"Antall menn: {count_male}")


class AgeQuestion(Question):
    def get_question(self, responses: ResponseTracker) -> str:
        return "Hvor gammel er du?"

    def is_valid_input(self, input_str: str) -> bool:
        return input_str.isdigit()

    def accept_input(self, input_str: str) -> tuple:
        return int(input_str), True

    def can_participate(self, responses: ResponseTracker):
        response = responses.get_answer_by_question(self)
        return 16 <= response <= 25

    def analyze(self, responses: list):
        age_sum = 0

        for age in responses:
            age_sum += age

        print(f"Gjennomsnittlig alder: {round(age_sum / len(responses), 1)}")


class YesNoQuestion(Question, ABC):
    def get_question(self, responses: ResponseTracker) -> str:
        return " [Ja/Nei]"

    def is_valid_input(self, input_str: str) -> bool:
        lower_case_str = input_str.lower()
        return lower_case_str == "ja" or lower_case_str == "nei"

    def accept_input(self, input_str: str) -> tuple:
        value = input_str.lower() == "ja"
        return value, True

    @abstractmethod
    def get_analyzation_prefix(self) -> str:
        pass

    def analyze(self, responses: list):
        count_subjects = 0
        participants = 0

        for response in responses:
            if response is None:
                continue

            participants += 1
            if response:
                count_subjects += 1

        print(f"{self.get_analyzation_prefix()}: {count_subjects} ({round((count_subjects / participants) * 100, 1)}%)")


class SubjectQuestion(YesNoQuestion):
    def get_question(self, responses: ResponseTracker) -> str:
        return f"Tar du et eller flere fag?{super().get_question(responses)}"

    def accept_input(self, input_str: str) -> tuple:
        value = input_str.lower() == "ja"
        return value, value

    def get_analyzation_prefix(self) -> str:
        return "Antall personer som tar fag"


class ITGKQuestion(YesNoQuestion):
    def get_question(self, responses: ResponseTracker) -> str:
        # Index 1 is age question
        if responses.get_answer_by_index(1) >= 22:
            return f"Tar virkelig du ITGK?{super().get_question(responses)}"
        return f"Tar du ITGK?{super().get_question(responses)}"

    def get_analyzation_prefix(self) -> str:
        return "Antall personer som tar ITGK"


class HomeworkQuestion(Question):
    def get_question(self, responses: ResponseTracker) -> str:
        return "Hvor mange timer bruker du daglig (i snitt, ca.) på lekser?"

    def is_valid_input(self, input_str: str) -> bool:
        try:
            float(input_str)
            return True
        except ValueError:
            return False

    def accept_input(self, input_str: str) -> tuple:
        return float(input_str), True

    def analyze(self, responses: list):
        count_homework = 0
        count_participant = 0

        for response in responses:
            if response is None:
                continue

            count_participant += 1
            count_homework += response

        print(f"Antall timer i snitt brukt på lekser: {round(count_homework / count_participant, 1)}")
