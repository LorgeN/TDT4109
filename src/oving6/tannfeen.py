from enum import Enum

# Constant for converting gram to monetary value
GRAM_VALUE = 1


class Coin(Enum):
    # Specify order, starting with largest for simpler implementation of Cashier's algorithm
    __order__ = 'TWENTY TEN FIVE ONE'

    TWENTY = 20, "Tjuere"
    TEN = 10, "Tiere"
    FIVE = 5, "Femere"
    ONE = 1, "Enere"


def find_coins(value: int) -> list:
    coins = []

    for coin in Coin:
        coins.append(value // coin.value[0])
        value %= coin.value[0]

    return coins


def format_coins(coins: list) -> str:
    formatted = []
    index = 0
    for coin in Coin:
        formatted.append(f"{coin.value[1]}: {coins[index]}")
        index += 1

    return ", ".join(formatted)


def find_coins_by_weight(weight: int) -> list:
    return find_coins(weight * GRAM_VALUE)


def find_coins_by_weights(weights: list) -> list:
    values = []

    for weight in weights:
        values.append(find_coins_by_weight(weight))

    return values


if __name__ == '__main__':
    # Sample test value
    teeth = [95, 103, 71, 99, 114, 64, 95, 53, 97, 114, 109, 11, 2, 21, 45, 2, 26, 81, 54, 14, 118, 108, 117, 27, 115,
             43, 70, 58, 107]

    for teeth_coins in find_coins_by_weights(teeth):
        print(format_coins(teeth_coins))
