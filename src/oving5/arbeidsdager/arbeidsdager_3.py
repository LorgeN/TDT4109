import arbeidsdager


def count_workdays(year: int) -> int:
    value = 52 * 5  # 52 weeks in a year, 5 days per week
    start_day = arbeidsdager.find_first_day(year)
    if arbeidsdager.is_workday(start_day + 1):
        value += 1

    if arbeidsdager.is_leap_year(year):
        value += 1

    return value


def main():
    for year in range(1900, 1920):
        print(f"{year} har {count_workdays(year)} arbeidsdager")


if __name__ == '__main__':
    main()
