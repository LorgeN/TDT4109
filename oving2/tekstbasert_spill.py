locked = True
complete = False


def walk_in():
    global complete
    if not locked:
        print("Du har kommet gjennom døren! Gratulerer!")
        complete = True
        return
    print("Døren er låst")


def knock():
    print("Ingen svarer :(")


def unlock():
    global locked
    if not locked:
        print("Døren er ikke låst")
        return
    locked = False
    print("Du låste opp døren!")


def is_complete():
    return complete


print("Det regner")
print("Du står utenfor en gul dør")

while not is_complete():
    # Convert to lowercase to make case insensitive
    command = input(">").lower()

    if command == "gå inn" or command == "gå inn døra":
        walk_in()
        continue

    if command == "bank på" or command == "bank på døra":
        knock()
        continue

    if command == "lås opp" or command == "lås opp døra":
        unlock()
        continue

    print("Ukjent kommando!")
