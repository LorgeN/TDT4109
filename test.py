def round_proper(value: str, desired_dec: int) -> float:
    """
    Rounds a given decimal value according to mathematical convention
    :rtype: float
    :param value: The given decimal, as a string
    :param desired_dec: The desired amount of decimals
    :return: The rounded value as a float
    """

    # Find where the decimals start, so we can round to the correct amount of decimals
    decimal_start = value.find('.')
    total = len(value)
    # If the number we are given does not contain a ., we assume that as "after" the given input
    if decimal_start == -1:
        decimal_start = total

    desired_round_point = decimal_start + desired_dec
    if desired_dec <= 0:
        # Subtract one to offset from decimal point
        desired_round_point = desired_round_point - 1

    # Ensure that we never set a max length that is shorter than the decimal point
    # Add one rounding point to account for . symbol in non-integers
    desired_length = max(decimal_start, desired_round_point + 1)

    # Use this variable and append each char as we find it
    result = ""

    # Iterate all chars in the desired range
    for i in range(desired_length):
        char = value[i]

        # Check if we are looking at a number previous to the point we want to round at
        if i < desired_round_point:
            result = result + char
            continue

        # Check if we are looking at a number after the point we want to round at
        if i > desired_round_point:
            result = result + "0"
            continue

        # We now know we are working with the char we want to round either up or leave as is.
        # To find this information, we need to know what the next digit is
        next_index = i + 1

        # If we are at the index just before the decimal point we need to skip that and consider the next index
        if next_index == decimal_start:
            next_index = next_index + 1

        round_val = int(value[next_index])
        if round_val >= 5:
            result = result + str(int(char) + 1)
            continue

        result = result + char
    return result


val = input("Skriv inn et desimaltall: ")
desiredDecimal = int(input("Antall desimlar etter avrunding: "))

output = round_proper(val, desiredDecimal)

print("Avrundet til", desiredDecimal, "desimaler:", output)
