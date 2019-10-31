import re
from collections import defaultdict


def read_from_file(filename):
    with open(filename) as file:
        return [line for line in file]


def remove_symbols(text):
    return re.sub(r'([^\s\w]|_)+', '', text.lower())


def count_words(filename):
    counts = defaultdict(int)
    with open(filename) as file:
        for line in file:
            words = remove_symbols(line.lower()).split(" ")
            for word in words:
                counts[word] += 1
    return dict(counts)


if __name__ == '__main__':
    print(count_words("alice_in_wonderland.txt"))
