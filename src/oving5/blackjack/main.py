from blackjack import BlackjackGame, MultiDeck


def start():
    print()
    print("Welcome to Python Text Based Blackjack v1.0!")
    print()

    deck_count_str = input("Please input the amount of card decks you'd like to play with: ")
    if not deck_count_str.isdigit():
        print(f"{deck_count_str} is not a number! Let's try again...")
        start()
        return

    deck_count = int(deck_count_str)
    player_count_str = input(f"Ok, cool, we'll play with {deck_count} decks. Now, how many players would you like? ")
    if not player_count_str.isdigit():
        print(f"{player_count_str} is not a number! Is it really that difficult? Let's try again...")
        start()
        return

    player_count = int(player_count_str)
    if player_count == 1:
        print("Playing all alone are we? Hmmm")

    print(f"Creating game with {deck_count} decks and {player_count} players...")
    game = BlackjackGame(MultiDeck(deck_count), player_count)
    game.play_new_round()

    while True:
        print()
        input_val = input("That was fun! Would you like to start a new round? [Yes/No]")
        if not input_val.lower() == "yes":
            print("I'll take that as a no.")
            break
        game.play_new_round()

    print()
    print("Game results!")
    print(f"Dealer: {game.dealer.get_balance()}")
    for player in game.players:
        print(f"{player.get_name()}: {player.get_balance()}")
    print()
    print("Thanks for playing!")


if __name__ == '__main__':
    start()
