from abc import ABC, abstractmethod
from enum import Enum
from random import shuffle


class CardColor(Enum):
    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    SPADES = 4


class CardRank(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


class Card:
    def __init__(self, rank: CardRank, color: CardColor):
        self.color = color
        self.rank = rank
        self.value = -1

    def get_rank(self) -> CardRank:
        return self.rank

    def get_color(self) -> CardColor:
        return self.color

    def get_value(self) -> list:
        if self.get_rank() == CardRank.ACE:
            return [1, 11]

        if self.get_rank() in [CardRank.JACK, CardRank.QUEEN, CardRank.KING]:
            return [10]

        return [self.get_rank().value]

    def add_value(self, existing: list) -> list:
        values = []
        for value in existing:
            for self_val in self.get_value():
                values.append(value + self_val)
        return values

    def get_name(self):
        return f"{self.get_rank().name.lower()} of {self.get_color().name.lower()}"


class CardProvider(ABC):
    @abstractmethod
    def get_random_card(self):
        pass

    @abstractmethod
    def get_cards_left(self) -> list:
        pass

    def get_count_remaining(self) -> int:
        return len(self.get_cards_left())

    def is_empty(self) -> bool:
        return self.get_count_remaining() == 0


class Deck(CardProvider):
    def __init__(self):
        self.cards = []
        self.add_deck()

    def add_deck(self):
        for color in CardColor:
            for rank in CardRank:
                self.cards.append(Card(rank, color))

    def get_random_card(self):
        self.ensure_not_empty()
        shuffle(self.cards)
        return self.cards.pop()

    def get_cards_left(self) -> list:
        return self.cards

    def ensure_not_empty(self):
        if len(self.cards) == 0:
            print("Out of cards in deck! Restocking...")
            self.add_deck()
            print("Restocking complete!")


class MultiDeck(Deck):
    def __init__(self, count: int):
        super().__init__()

        self.count = count

        for i in range(count - 1):
            self.add_deck()

    def ensure_not_empty(self):
        if len(self.cards) == 0:
            print("Out of cards in deck! Restocking...")
            for i in range(self.count):
                self.add_deck()
            print("Restocking complete!")
