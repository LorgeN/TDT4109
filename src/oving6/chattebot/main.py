from chattebot import *


def print_intro_text():
    print("\n" * 20)
    print("Hei, jeg heter HAL og vil gjerne snakke med deg.")
    print("Bruk hele setninger. Skriv 'hade' hvis du vil avslutte samtalen")
    print("**************************************************")
    print()


def main():
    print_intro_text()

    responses = UserResponses()

    responses.take_input(NAME_QUESTION)

    continue_loop = True
    while continue_loop:
        question = select_response(QUESTIONS, responses)
        continue_loop = responses.take_input(question)

        follow_up = select_response(FOLLOW_UP_QUESTIONS, responses)
        responses.take_input(follow_up)

        remark = select_response(REMARKS, responses)
        print(remark.get_sentence(responses))


if __name__ == '__main__':
    main()
