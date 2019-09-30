from sporreundersokelsen import *


def main():
    form = Form([GenderQuestion(), AgeQuestion(), SubjectQuestion(), ITGKQuestion(), HomeworkQuestion()])

    while True:
        form.new_participant()


if __name__ == '__main__':
    main()
