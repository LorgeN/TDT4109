DAYS_OF_WEEK = ["man", "tir", "ons", "tor", "fre", "lor", "son"]


def get_name(day_of_week: int) -> str:
    return DAYS_OF_WEEK[day_of_week % 7]


def is_leap_year(year: int) -> int:
    return year % 400 == 0 or (not year % 100 == 0 and year % 4 == 0)


def find_first_day(year: int) -> int:
    # Start at 1900
    day = 0
    diff = year - 1900
    if diff is 0:
        return day

    # Could calculate leap years between 1900 and year, which would be faster
    if diff > 0:
        for y in range(1901, year + 1):
            day = (day + (2 if is_leap_year(y - 1) else 1)) % 7
    else:
        # Untested but not required to complete task (Also no data to test against)
        for y in range(1899, year, -1):
            day = (day - (2 if is_leap_year(y - 1) else 1)) % 7
    return day


def main():
    for year in range(1900, 1920):
        print(f"{year}: {get_name(find_first_day(year))}")


if __name__ == '__main__':
    main()
