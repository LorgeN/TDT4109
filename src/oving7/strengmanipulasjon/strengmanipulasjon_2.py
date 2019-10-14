from strengmanipulasjon import find_substring_indexes


def replace(search_str, target_str, substitute):
    indices = find_substring_indexes(search_str, target_str)
    search_length = len(search_str)

    last_index = 0
    strings = []
    for index in indices:
        strings.append(target_str[last_index:index])
        last_index = index + search_length
        strings.append(substitute)

    return "".join(strings)


if __name__ == '__main__':
    print(replace("iS", "Is this the real life? Is this just fantasy?", "cool"))
    print(replace("oo", "Never let you goooo let me goo. Never let me goo oooo", "cool"))
