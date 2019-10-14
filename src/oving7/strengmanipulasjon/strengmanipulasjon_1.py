import re


def find_substring_indexes(search_str, string_to_search):
    return [m.start() for m in re.finditer(f"(?={search_str})", string_to_search, re.IGNORECASE)]


if __name__ == '__main__':
    print(find_substring_indexes("iS", "Is this the real life? Is this just fantasy?"))
    print(find_substring_indexes("oo", "Never let you go let me go. Never let me go ooo"))
