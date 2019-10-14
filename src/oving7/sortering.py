def bubble_sort(collection):
    n = len(collection)

    for i1 in range(n):
        # Last i1 elements will already be in place because we've compared them earlier. In addition,
        # we subtract one to avoid index out of bounds on last check
        for i2 in range(n - i1 - 1):
            val1 = collection[i2]
            val2 = collection[i2 + 1]
            if val1 <= val2:
                continue

            collection[i2] = val2
            collection[i2 + 1] = val1

    return collection


def selection_sort(collection):
    n = len(collection)

    # Consider each element but last one since it should be automatically sorted. Reverse order iterate,
    # find highest, move to top of list
    for i1 in range(n - 1, 0, -1):
        highest = -1, -1
        for i2 in range(i1 + 1):
            val = collection[i2]
            if val < highest[0]:
                continue

            highest = val, i2

        # Swap them
        curr_val = collection[i1]
        collection[i1] = highest[0]
        collection[highest[1]] = curr_val

    return collection
