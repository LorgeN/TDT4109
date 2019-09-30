import arbeidsdager


def is_workday(day: int) -> int:
    return (day % 7) < 5


def main():
    # Run a quick test
    for day in range(7):
        print(f"Is {arbeidsdager.get_name(day)} a workday? = {is_workday(day)}")


if __name__ is "__main__":
    main()
