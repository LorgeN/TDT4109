from enum import Enum
import re

COORD_VALIDATION = re.compile("[1-3],( )*[1-3]")

WINNER_PATTERNS = [
    # Horizontal wins
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
    # Vertical wins
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
    # Diagonal
    [(0, 0), (1, 1), (2, 2)],
    [(2, 0), (1, 1), (0, 2)]
]


class SlotValue(Enum):
    NONE = ' '
    CROSS = 'X'
    CIRCLE = 'O'


class Board:
    __slots__ = "board"

    def __init__(self):
        # Use for instead of * to avoid same reference
        self.board = [[SlotValue.NONE for i in range(3)] for i in range(3)]

    def print_board(self):
        print(f"  {''.join([str(i).rjust(4) for i in range(1, 4)])}")
        print(f"   {''.join(['-'] * 12)}")

        for line_index in range(3):
            print(f" {line_index + 1} | {' | '.join(slot.value for slot in self.board[line_index])} |")
            print(f"   {''.join(['-']) * 12}")

    def get_value(self, x, y):
        return self.board[y][x]

    def set_value(self, x, y, value):
        self.board[y][x] = value

    def get_winner(self):
        for pattern in WINNER_PATTERNS:
            base_val = self.get_value(pattern[0][0], pattern[0][1])
            error = False
            for i in range(1, 3):
                curr_val = self.get_value(pattern[i][0], pattern[i][1])
                if not curr_val == base_val:
                    error = True
                    break
            if not error:
                return base_val
        return SlotValue.NONE

    def is_full(self):
        for line in self.board:
            for slot in line:
                if slot == SlotValue.NONE:
                    return False
        return True


def accept_input(board, value):
    board.print_board()
    coords_str = input(f"Player {value.value}, please enter a coordinate:")
    if not COORD_VALIDATION.match(coords_str):
        print("Invalid input! Please enter input in the form 'x, y'!")
        accept_input(board, value)
        return

    parts = coords_str.split(",")
    x = int(parts[0].strip()) - 1
    y = int(parts[1].strip()) - 1
    if not board.get_value(x, y) == SlotValue.NONE:
        print("Invalid slot! Please enter another slot!")
        accept_input(board, value)
        return

    board.set_value(x, y, value)

    winner = board.get_winner()
    if not winner == SlotValue.NONE:
        print(f"Congratulations, {winner.value}, you have won!")
        exit()


if __name__ == '__main__':
    print("Welcome to tic tac toe!")
    board = Board()

    current_player = SlotValue.CROSS
    while (not board.is_full()) and board.get_winner() == SlotValue.NONE:
        accept_input(board, current_player)
        current_player = SlotValue.CIRCLE if current_player == SlotValue.CROSS else SlotValue.CROSS

    if board.is_full():
        print("That's a tie!")
