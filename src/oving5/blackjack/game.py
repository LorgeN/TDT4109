from blackjack import Card, CardProvider
from abc import ABC, abstractmethod
from enum import Enum
import random

RICH_TECH_PEOPLE = ["Jeff Bezos", "Bill Gates", "Elon Musk", "Mark Zuckerberg", "Larry Page"]


class BlackjackAction(Enum):
    HIT = 1
    STAY = 2

    @staticmethod
    def from_string(string: str):
        if string.lower() == "hit":
            return BlackjackAction.HIT
        if string.lower() == "stay":
            return BlackjackAction.STAY
        return None


class Hand:
    def __init__(self, card1: Card, card2: Card):
        self.cards = [card1, card2]

    def get_highest_value(self) -> int:
        high_val = -1
        for value in self.get_values():
            if high_val < value:
                high_val = value
        return high_val

    def get_values(self) -> list:
        values = self.cards[0].get_value()
        for card in self.cards[1::]:
            values = card.add_value(values)
        return values

    def add_card(self, provider: CardProvider) -> Card:
        card = provider.get_random_card()
        self.cards.append(card)
        return card

    def is_bust(self) -> bool:
        for value in self.get_values():
            if value <= 21:
                return False
        return True

    def is_blackjack(self) -> bool:
        if not len(self.cards) == 2:
            return False

        for value in self.get_values():
            if value == 21:
                return True
        return False

    def get_card_names(self) -> str:
        return ", ".join(card.get_name() for card in self.cards)

    def get_value_names(self) -> str:
        return " or ".join(self.get_values())


class Participant(ABC):
    def __init__(self, balance: int):
        super().__init__()
        self.balance = balance

    @abstractmethod
    def get_action(self, hand) -> BlackjackAction:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    def get_balance(self) -> int:
        return self.balance

    def set_balance(self, balance: int):
        self.balance = balance

    def subtract_balance(self, balance: int) -> int:
        self.balance -= balance
        return self.balance

    def add_balance(self, balance: int) -> int:
        self.balance += balance
        return self.balance


class Dealer(Participant):
    def get_action(self, hand) -> BlackjackAction:
        # Dealer draws til 16, and stands on 17
        for value in hand.get_values():
            if value > 16:
                return BlackjackAction.STAY
        return BlackjackAction.HIT

    def get_name(self) -> str:
        return "Dealer"


class Player(Participant):
    def __init__(self, name: str, balance: int):
        super().__init__(balance)
        self.name = name

    def get_action(self, hand) -> BlackjackAction:
        print("Please enter action to execute:")
        for action in BlackjackAction:
            print(f"  - {action.value}: {action.name}")

        input_str = input("Enter action: ")
        action = BlackjackAction.from_string(input_str)

        if action is None:
            # Invalid action, let's ask for another one
            print(f"Invalid action {input_str}!")
            return self.get_action(hand)

        return action

    def get_name(self) -> str:
        return self.name


class BlackjackGame:
    def __init__(self, provider: CardProvider, player_count: int):
        self.provider = provider
        self.dealer = Dealer(10000)
        self.players = [Player(input(f"Enter player #{i}'s name: "), 500) for i in range(1, player_count + 1)]

    def get_participant_count(self) -> int:
        return len(self.players)

    def play_new_round(self):
        print("Starting new round!")

        for player in self.players:
            if player.get_balance() > 100:
                continue

            print(f"Oh no! {player.get_name()}'s balance is low!")
            benefactor = RICH_TECH_PEOPLE[random.randint(0, len(RICH_TECH_PEOPLE) - 1)]
            amount = random.randint(300, 1000)
            print(f"But don't worry, {benefactor} has a lot of faith in him/her (and a lot of money), and"
                  f" has graciously given them another {amount} to play with!")
            player.add_balance(amount)

        BlackjackRound(self).play()


class BlackjackOutcome(Enum):
    LOSS = 0
    PUSH = 1
    WIN = 2
    BLACKJACK = 2.5

    def get_multiplier(self) -> float:
        return self.value


class BlackjackRound:
    def __init__(self, game: BlackjackGame):
        self.game = game
        self.bets = [0] * game.get_participant_count()
        self.dealer_hand = Hand(game.provider.get_random_card(), game.provider.get_random_card())
        self.hands = [Hand(game.provider.get_random_card(), game.provider.get_random_card()) for player in game.players]

    def play(self):
        self.handle_bets()
        self.handle_hands()
        self.handle_outcomes()

    def handle_bets(self):
        for player in self.game.players:
            self.handle_bet(player)
            print()
        print(f"Bets have been placed!")

    def handle_bet(self, player: Player):
        print(f"{player.get_name()}, you have a balance of {player.get_balance()}.")
        bet_str = input("Please place your bet: ")
        if not bet_str.isdigit():
            print(f"Invalid input {bet_str}! Please enter a number.")
            self.handle_bet(player)
            return

        bet = int(bet_str)
        if bet > player.get_balance():
            print(f"{bet} exceeds your balance! Please enter a lower number.")
            self.handle_bet(player)
            return

        self.bets[self.game.players.index(player)] = bet
        self.game.dealer.add_balance(bet)
        print(f"Bet {bet} placed! Your balance is now {player.subtract_balance(bet)}")

    def handle_hands(self):
        print()
        print(f"Dealer has {self.dealer_hand.cards[0].get_name()} and ?")
        print()

        for player in self.game.players:
            self.handle_hand(player, self.hands[self.game.players.index(player)])

        print()
        print("Dealer plays.")
        print()
        self.handle_hand(self.game.dealer, self.dealer_hand)
        print()
        print("All hands played.")

    def handle_hand(self, participant: Participant, hand: Hand):
        print(f"{participant.get_name()} has {hand.get_card_names()}, for value(s) {hand.get_values()}")
        if hand.is_blackjack():
            print(f"{participant.get_name()} has blackjack!")
            return

        if hand.get_highest_value() == 21:
            print(f"{participant.get_name()} has 21!")
            return

        action = participant.get_action(hand)
        if action == BlackjackAction.STAY:
            print(f"{participant.get_name()} has chosen to stay.")
            return

        print(f"{participant.get_name()} has chosen to hit")
        card = hand.add_card(self.game.provider)
        print(f"{card.get_name()} was drawn")
        if hand.is_bust():
            print(f"{participant.get_name()} has busted")
            return

        self.handle_hand(participant, hand)

    def get_outcome(self, player: Player) -> BlackjackOutcome:
        hand = self.hands[self.game.players.index(player)]
        print(f"{player.get_name()} has {hand.get_card_names()}, for a high value of {hand.get_highest_value()}")

        if hand.is_bust():
            return BlackjackOutcome.LOSS

        if hand.is_blackjack():
            return BlackjackOutcome.BLACKJACK if not self.dealer_hand.is_blackjack() else BlackjackOutcome.PUSH

        if self.dealer_hand.is_bust():
            return BlackjackOutcome.WIN

        if self.dealer_hand.is_blackjack():
            return BlackjackOutcome.LOSS

        dealer_val = self.dealer_hand.get_highest_value()
        player_val = hand.get_highest_value()
        if dealer_val == player_val:
            return BlackjackOutcome.PUSH

        return BlackjackOutcome.WIN if dealer_val < player_val else BlackjackOutcome.LOSS

    def handle_outcomes(self):
        print()

        for player in self.game.players:
            self.handle_outcome(player)
            if self.game.dealer.get_balance() > 0:
                continue
            print("OH NO! The dealer is out of money! Casino is shutting down :'(")
            exit(0)

    def handle_outcome(self, player: Player):
        outcome = self.get_outcome(player)

        print(f"Outcome for {player.get_name()} is {outcome.name}")

        amount_to_add = int(self.bets[self.game.players.index(player)] * outcome.get_multiplier())
        # Only inform player if they actually got a reward
        if amount_to_add > 0:
            print(f"Prize is {amount_to_add}.")

        print(f"New balance is {player.add_balance(amount_to_add)}")
        self.game.dealer.subtract_balance(amount_to_add)
