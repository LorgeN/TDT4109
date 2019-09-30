from abc import ABC, abstractmethod
from sys import exit


class Form:
    def __init__(self, questions: list):
        self.questions = questions
        self.responses = []

    def new_participant(self):
        tracker = ResponseTracker(self)

        print("")
        print("Velkommen til spørreundersøkelsen!")
        print(f"Du er deltaker #{len(self.responses) + 1}")
        print("")

        for question in self.questions:
            result = tracker.ask_question(question)
            if not result[1]:
                print("  Du kan dessverre ikke ta denne undersøkelsen")
                # Can't participate
                return
            if not result[0]:
                # Doesn't need to answer following questions
                break
        self.responses.append(tracker)

    def analyze(self):
        print("Resultat av undersøkelse:")
        for question in self.questions:
            responses = []
            for response in self.responses:
                responses.append(response.get_answer_by_question(question))
            question.analyze(responses)


class ResponseTracker:
    def __init__(self, form: Form):
        self.form = form
        self.answers = [None] * len(form.questions)

    def ask_question(self, question) -> tuple:
        # Remove trailing and leading whitespace for improved input validation
        input_val = input(f"  {question.get_question(self)} ").strip()

        # Check for global escape
        if input_val.lower() == "hade":
            print("")
            print("Avslutter undersøkelse...")
            print("")
            self.form.analyze()
            exit(0)

        # Check if input is valid, if not, ask again
        if not question.is_valid_input(input_val):
            print(f"  Ugyldig input '{input_val}'!")
            return self.ask_question(question)

        parsed_input = question.accept_input(input_val)
        self.set_answer(question, parsed_input[0])
        return parsed_input[1], question.can_participate(self)

    def get_question(self, index: int) -> object:
        return self.form.questions[index]

    def get_index(self, question) -> int:
        return self.form.questions.index(question)

    def get_answer_by_index(self, index: int) -> object:
        return self.answers[index]

    def get_answer_by_question(self, question):
        return self.get_answer_by_index(self.form.questions.index(question))

    def set_answer(self, question, answer):
        self.answers[self.form.questions.index(question)] = answer


class Question(ABC):
    @abstractmethod
    def get_question(self, responses: ResponseTracker) -> str:
        """
        Specifies this question as a readable string for the user to comprehend, e.g. "How old are you?". May also
        contain hints specifying accepted values, e. g. for a yes/no question
        :return: This question as a user friendly string
        """
        pass

    @abstractmethod
    def is_valid_input(self, input_str: str) -> bool:
        """
        Checks if the given input is a valid input for this question. If not valid, the question will be asked again
        :param input_str: The string the user has given
        :return: A boolean specifying if the input is valid or not
        """
        pass

    @abstractmethod
    def accept_input(self, input_str: str) -> tuple:
        """
        Accepts the input, and parses it into the type this question uses to store answers, e. g. an int
        :param input_str: The string the user has given
        :return: A tuple containing the parsed value, and a boolean value specifying if we should proceed to
        """
        pass

    def can_participate(self, responses: ResponseTracker) -> bool:
        """
        Overridable method determining if the participant may part take in this form based on the given answer. If
        the result is False, the form will stop at this point and not include the already provided responses in the
        final analysis/statistics. This method will be called after accept_input()
        :param responses: The already provided response (None for questions after this one).
        :return: If the participant can participate in this form
        """
        return True

    @abstractmethod
    def analyze(self, responses: list):
        """
        Performs any analysis this question would like to do based on the answers given by all participants. No return
        value, method should directly print any relevant results
        :param responses: The responses given by the participants
        """
        pass
