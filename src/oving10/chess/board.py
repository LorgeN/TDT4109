from tkinter import messagebox

import pygame as game
from sys import exit
from pygame.draw import rect
from pygame.display import set_mode
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from enum import Enum
from abc import ABC, abstractmethod
from tkinter import *

GRID_SIZE = 8
SCREEN_SIZE = 640

LIGHT_BROWN = (251, 196, 117)
DARK_BROWN = (139, 69, 0)
GRAY = (100, 100, 100)
VIOLET = (238, 130, 238)
HIGHLIGHT = [(0, 255, 0), (0, 255, 125)]


def get_grid_position(pos):
    square_size = SCREEN_SIZE // GRID_SIZE
    x = pos[0] // square_size
    y = pos[1] // square_size
    return Position(x, y)


class Direction(Enum):
    UP = 0, -1
    DOWN = 0, 1
    RIGHT = 1, 0
    LEFT = -1, 0
    UP_RIGHT = 1, -1
    UP_LEFT = -1, -1
    DOWN_RIGHT = 1, 1
    DOWN_LEFT = -1, 1

    @property
    def x(self):
        return self.value[0]

    @property
    def y(self):
        return self.value[1]


class Position:
    __slots__ = "x", "y"

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def top_left(self):
        multiplier = SCREEN_SIZE // GRID_SIZE
        return (self.x * multiplier) - 1, (self.y * multiplier) - 1

    @property
    def center(self):
        multiplier = SCREEN_SIZE // GRID_SIZE
        half_multip = multiplier // 2
        return self.x * multiplier + half_multip, self.y * multiplier + half_multip

    def is_valid(self):
        return 0 <= self.x < GRID_SIZE and 0 <= self.y < GRID_SIZE

    def move(self, dir, count=1):
        if count == 1:
            return Position(self.x + dir.x, self.y + dir.y)

        pos = self.move(dir)
        if count == -1:
            positions = []
            while pos.is_valid():
                positions.append(pos)
                pos = pos.move(dir)
            return positions

        positions = []
        for i in range(count):
            positions.append(pos)
            pos = pos.move(dir)
        return positions

    def __eq__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return other.x == self.x and other.y == self.y


class BaseBoard:
    __slots__ = "pieces", "screen"

    def __init__(self):
        self.pieces = [([None] * GRID_SIZE) for i in range(GRID_SIZE)]

    def print(self):
        for row in self.pieces:
            for piece in row:
                if not piece:
                    print("(  )", end="")
                else:
                    print("(" + piece.color.name[0] + piece.piece_type.name[0] + ")", end="")
            print()

    def is_check(self, color):
        self.print()
        king = None
        enemy_pieces = []
        for piece in self.get_pieces():
            if not piece.color == color:
                enemy_pieces.append(piece)
            elif piece.piece_type == PieceType.KING:
                king = piece

        for enemy_piece in enemy_pieces:
            moves = enemy_piece.get_legal_moves(self)
            if king.position in moves:
                print(enemy_piece.color, enemy_piece.piece_type, "puts", color, "in check")
                return True
        return False

    def get_piece_at(self, pos):
        grid_pos = get_grid_position(pos)
        return self.get_piece(grid_pos.x, grid_pos.y)

    def get_pieces(self):
        pieces = []
        for row in self.pieces:
            for piece in row:
                if piece is None:
                    continue
                pieces.append(piece)
        return pieces

    def get_piece(self, x, y):
        return self.pieces[y][x]

    def move_piece(self, from_pos, to_pos):
        piece = self.get_piece(from_pos.x, from_pos.y)
        self.set_piece(to_pos.x, to_pos.y, piece)

    def set_piece(self, x, y, piece):
        self.pieces[piece.position.y][piece.position.x] = None
        self.pieces[y][x] = piece
        piece.position = Position(x, y)
        if isinstance(piece, DummyPiece):
            return

        piece.reset()

    def is_valid_position(self, x, y, piece):
        curr_piece = self.get_piece(x, y)
        if not curr_piece:
            return True
        return not curr_piece.color == piece.color

    def dummy_clone(self):
        board = BaseBoard()
        board.pieces = [[piece.as_base() if piece else None for piece in row] for row in self.pieces]
        return board


class Board(BaseBoard):
    def __init__(self):
        super().__init__()
        self.screen = set_mode((SCREEN_SIZE, SCREEN_SIZE))

    def is_checkmate(self, color):
        for piece in self.get_pieces():
            if not piece.color == color:
                continue

            if len(piece.get_legal_moves(self)) > 0:
                return False
        return True

    def set_default(self):
        self.__new_piece(0, 0, Color.BLACK, PieceType.ROOK)
        self.__new_piece(7, 0, Color.BLACK, PieceType.ROOK)
        self.__new_piece(0, 7, Color.WHITE, PieceType.ROOK)
        self.__new_piece(7, 7, Color.WHITE, PieceType.ROOK)

        self.__new_piece(1, 0, Color.BLACK, PieceType.KNIGHT)
        self.__new_piece(6, 0, Color.BLACK, PieceType.KNIGHT)
        self.__new_piece(1, 7, Color.WHITE, PieceType.KNIGHT)
        self.__new_piece(6, 7, Color.WHITE, PieceType.KNIGHT)

        self.__new_piece(2, 0, Color.BLACK, PieceType.BISHOP)
        self.__new_piece(5, 0, Color.BLACK, PieceType.BISHOP)
        self.__new_piece(2, 7, Color.WHITE, PieceType.BISHOP)
        self.__new_piece(5, 7, Color.WHITE, PieceType.BISHOP)

        self.__new_piece(3, 0, Color.BLACK, PieceType.QUEEN)
        self.__new_piece(4, 0, Color.BLACK, PieceType.KING)

        self.__new_piece(3, 7, Color.WHITE, PieceType.QUEEN)
        self.__new_piece(4, 7, Color.WHITE, PieceType.KING)

        for x in range(GRID_SIZE):
            self.__new_piece(x, 1, Color.BLACK, PieceType.PAWN)
            self.__new_piece(x, 6, Color.WHITE, PieceType.PAWN)

    def __new_piece(self, x, y, color, type):
        pos = Position(x, y)
        self.set_piece(x, y, Piece(color, type, pos))

    def draw_board(self, colors, highlight=None):
        self.screen.fill((255, 255, 255))

        incr = SCREEN_SIZE / GRID_SIZE

        index = 1
        for column in range(GRID_SIZE):
            for row in range(GRID_SIZE):
                color = colors[index]
                if highlight and Position(row, column) in highlight:
                    color = HIGHLIGHT[index]

                sqr = game.Rect(row * incr, column * incr, incr + 1, incr + 1)
                rect(self.screen, color, sqr)

                index += 1
                index %= 2

            index += 1
            index %= 2

    def draw_pieces(self):
        for piece in self.get_pieces():
            piece.draw(self.screen)


def _verify_simple_list(board, pos_list, piece):
    return [pos for pos in pos_list if pos.is_valid() and board.is_valid_position(pos.x, pos.y, piece)]


def _verify_continuous_list(board, pos_list, piece):
    ret_list = []
    for pos in pos_list:
        curr_piece = board.get_piece(pos.x, pos.y)
        if not curr_piece:
            ret_list.append(pos)
            continue

        if curr_piece.color == piece.color:
            return ret_list

        ret_list.append(pos)
        return ret_list
    return ret_list


class PieceMovement(ABC):
    @abstractmethod
    def get_possible_moves(self, board, pos, piece):
        pass


class KingMovement(PieceMovement):
    def get_possible_moves(self, board, pos, piece):
        return _verify_simple_list(board, [pos.move(direct) for direct in Direction], piece)


class QueenMovement(PieceMovement):
    def get_possible_moves(self, board, pos, piece):
        complete_movement = [pos.move(direct, count=-1) for direct in Direction]
        ret_list = []
        for dir_list in complete_movement:
            ret_list += _verify_continuous_list(board, dir_list, piece)
        return ret_list


class RookMovement(PieceMovement):
    def get_possible_moves(self, board, pos, piece):
        directions = [Direction.UP, Direction.DOWN, Direction.RIGHT, Direction.LEFT]
        complete_movement = [pos.move(direct, count=-1) for direct in directions]
        ret_list = []
        for dir_list in complete_movement:
            ret_list += _verify_continuous_list(board, dir_list, piece)
        return ret_list


class BishopMovement(PieceMovement):
    def get_possible_moves(self, board, pos, piece):
        directions = [Direction.UP_RIGHT, Direction.UP_LEFT, Direction.DOWN_RIGHT, Direction.DOWN_LEFT]
        ret_list = []
        for direction in directions:
            ret_list += _verify_continuous_list(board, pos.move(direction, count=-1), piece)
        return ret_list


KNIGHT_OFFSETS = [(-1, 2), (1, 2), (-2, 1), (2, 1), (-1, -2), (1, -2), (-2, -1), (2, -1)]


class KnightMovement(PieceMovement):
    def get_possible_moves(self, board, pos, piece):
        positions = [Position(pos.x + offset[0], pos.y + offset[1]) for offset in KNIGHT_OFFSETS]
        return _verify_simple_list(board, [position for position in positions if position.is_valid()], piece)


PAWN_WHITE_OFFSETS = [Direction.UP_LEFT.value, Direction.UP_RIGHT.value]
PAWN_BLACK_OFFSETS = [Direction.DOWN_LEFT.value, Direction.DOWN_RIGHT.value]


class PawnMovement(PieceMovement):
    def get_possible_moves(self, board, pos, piece):
        direction = Direction.UP if piece.color == Color.WHITE else Direction.DOWN
        positions = [pos.move(direction)]
        if piece.starting_position == pos:
            positions.append(positions[0].move(direction))

        positions = [position for position in positions if
                     position.is_valid() and not board.get_piece(position.x, position.y)]

        offsets = PAWN_WHITE_OFFSETS if piece.color == Color.WHITE else PAWN_BLACK_OFFSETS
        for offset in offsets:
            new_pos = Position(pos.x + offset[0], pos.y + offset[1])
            if not new_pos.is_valid():
                continue

            piece_at = board.get_piece(new_pos.x, new_pos.y)
            if not piece_at or piece_at.color == piece.color:
                continue
            positions.append(new_pos)
        return positions


class Color(Enum):
    WHITE = 0
    BLACK = 1

    @property
    def other(self):
        return Color.WHITE if self == Color.BLACK else Color.BLACK

    @property
    def name(self):
        if self == Color.WHITE:
            return "White"
        return "Black"

    def __eq__(self, other):
        if not isinstance(other, Color):
            return NotImplemented
        return other.value == self.value


class PieceType(Enum):
    KING = 'King.png', KingMovement()
    QUEEN = 'Queen.png', QueenMovement()
    ROOK = 'Rook.png', RookMovement()
    BISHOP = 'Bishop.png', BishopMovement()
    KNIGHT = 'Knight.png', KnightMovement()
    PAWN = 'Pawn.png', PawnMovement()

    @property
    def file_suffix(self):
        return self.value[0]

    @property
    def movement(self):
        return self.value[1]

    @property
    def black_sprite(self):
        return f"sprite\\Black{self.file_suffix}"

    @property
    def white_sprite(self):
        return f"sprite\\White{self.file_suffix}"


class DummyPiece:
    def __init__(self, color, piece_type, position):
        self.color = color
        self.piece_type = piece_type
        self.starting_position = position
        self.position = position

    def get_legal_moves(self, board):
        return self.piece_type.movement.get_possible_moves(board, self.position, self)

    def as_base(self):
        return DummyPiece(self.color, self.piece_type, self.position)


class Piece(game.sprite.Sprite):
    def __init__(self, color, piece_type, position):
        super().__init__()

        self.color = color
        self.piece_type = piece_type

        sprite_path = piece_type.black_sprite if color == Color.BLACK else piece_type.white_sprite
        dimensions = SCREEN_SIZE // 8, SCREEN_SIZE // 8
        self.image = game.transform.scale(game.image.load(sprite_path), dimensions)

        self.starting_position = position
        self.position = position

        self.background = game.Rect(self.image.get_rect())
        self.background.topleft = position.top_left
        self.background.center = position.center

    def set_type(self, type):
        self.piece_type = type

        sprite_path = type.black_sprite if self.color == Color.BLACK else type.white_sprite
        dimensions = SCREEN_SIZE // 8, SCREEN_SIZE // 8
        self.image = game.transform.scale(game.image.load(sprite_path), dimensions)

    def get_legal_moves(self, board):
        print("Checking moves for", self.color, self.piece_type)
        moves = self.piece_type.movement.get_possible_moves(board, self.position, self)
        print("Found", len(moves), "moves")
        legal_moves = []
        dummy_board = board.dummy_clone()
        for move in moves:
            dummy_board.move_piece(self.position, move)
            if not dummy_board.is_check(self.color):
                legal_moves.append(move)
                print("Found legal move")
            dummy_board.move_piece(move, self.position)
        print("Found", len(legal_moves), "legal moves for", self.color, self.piece_type)
        return legal_moves

    def as_base(self):
        return DummyPiece(self.color, self.piece_type, self.position)

    def draw(self, surface):
        surface.blit(self.image, self.background.topleft)

    def drag(self, cursor):
        self.background.center = cursor

    def reset(self):
        self.background.center = self.position.center

    def update(self, position):
        self.position = position
        self.background.center = position.center


PROMOTIONS = [PieceType.QUEEN, PieceType.KNIGHT, PieceType.ROOK, PieceType.BISHOP]


class PromotionDialog:
    __slots__ = "toplevel", "listbox", "value"

    def __init__(self, parent):
        self.toplevel = Toplevel(parent)
        self.value = None

        names = StringVar(value=[promotion.name for promotion in PROMOTIONS])

        label = Label(self.toplevel, text="Pick a type")
        self.listbox = Listbox(self.toplevel, listvariable=names, height=3, selectmode=SINGLE, exportselection=0)
        button = Button(self.toplevel, text="Confirm", command=self.toplevel.destroy)

        label.pack(side="top", fill="x")
        self.listbox.pack(side="top", fill="x")
        button.pack()

        self.listbox.bind('<<ListboxSelect>>', self.get_selection)

    def get_selection(self, event):
        widget = event.widget
        selection = widget.curselection()
        self.value = widget.get(selection[0])

    def return_value(self):
        self.toplevel.wait_window()
        return self.value


def select_promotion():
    try:
        return PieceType[PromotionDialog(Frame()).return_value()]
    except:
        return PieceType.QUEEN


def new_game():
    # Hide main window of tkinter
    Tk().wm_withdraw()

    board = Board()
    board.draw_board([DARK_BROWN, LIGHT_BROWN])
    board.set_default()
    board.draw_pieces()

    fps = game.time.Clock()

    game.display.set_caption("60FPS Chess")
    game.display.update()

    target_piece = None
    turn = Color.WHITE
    mouse_down = False
    mouse_released = False
    legal_moves = None
    show_check = False

    while True:
        if board.is_checkmate(turn):
            board.draw_board([GRAY, VIOLET], legal_moves)
            board.draw_pieces()
            game.display.flip()

            messagebox.showinfo("Checkmate!", f"{turn.other.name} wins")
            break

        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_down = True
            elif event.type == MOUSEBUTTONUP:
                mouse_down = False
                mouse_released = True

        cursor = game.mouse.get_pos()

        if mouse_down and not target_piece:
            target_piece = board.get_piece_at(cursor)
            if target_piece:
                if not target_piece.color == turn:
                    target_piece = None
                else:
                    legal_moves = target_piece.get_legal_moves(board)
        elif mouse_down and target_piece:
            target_piece.drag(cursor)
        elif mouse_released and target_piece:
            grid_pos = get_grid_position(cursor)
            if grid_pos in legal_moves:
                board.set_piece(grid_pos.x, grid_pos.y, target_piece)
                turn = turn.other

                if target_piece.piece_type == PieceType.PAWN:
                    # Can't move backwards, no need for color check
                    if grid_pos.y == 0 or grid_pos.y == 7:
                        target_piece.set_type(select_promotion())

                if board.is_check(turn) and not board.is_checkmate(turn):
                    show_check = True
            else:
                target_piece.reset()
            target_piece = None
            legal_moves = None

        board.draw_board([DARK_BROWN, LIGHT_BROWN], legal_moves)
        board.draw_pieces()

        game.display.flip()

        # Show box here after rendering to avoid "frozen" state
        if show_check:
            messagebox.showinfo("Check", f"{turn.name}'s king is under check")
            show_check = False

        fps.tick(60)

    # Prevent program from not responding, and allow the user to graciously close it
    while True:
        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                exit()


if __name__ == '__main__':
    new_game()
