from copy import deepcopy
from Node import Node

class Board:
    
    def __init__(self):
        self.counter = 0
        self.board_width = 7
        self.board_height = 6
        self.board = [list(".......") for _ in range(self.board_height)]
        self.y_coords = {col: self.board_height - 1 for col in range(self.board_width)}
        self.last_move_column = None


    def to_tuple(self):
        return tuple(tuple(row) for row in self.board)
    
    def get_simulation_board(self):
        return []

    def print_board(self):
        print("\n" + " ".join(map(str, [1, 2, 3, 4, 5, 6, 7])))
        for row in self.board:
            print(" ".join(row))
        print()

    def is_empty(self, x, y) -> bool:
        # Simply check if the current position is empty
        return self.board[y][x] == "."
    
    def is_board_full(self) -> bool:
        return self.counter == 42
    
    def is_legal_move(self, x) -> bool:
        if self.is_board_full():
            return False
        if not 0 <= x < self.board_width:
            return False  # OUT OF BOUNDS
        if self.y_coords[x] < 0:
            return False  # COLUMN IS FULL
        return self.is_empty(x, self.y_coords[x])

    def make_move(self, x, current_player):
        y = self.y_coords[x]
        self.board[y][x] = current_player  # makes the move
        self.counter += 1  # increase the counter
        self.y_coords[x] -= 1
        self.last_move_column = x



        # WIN CONDITION CHECK
        # Função auxiliar para contar peças em uma direção
    def count_in_direction(self, current_player, dx, dy, x, y):
        count = 0
        while (0 <= x + dx < self.board_width and 
            0 <= y + dy < self.board_height and 
            self.board[y + dy][x + dx] == current_player):
            x += dx
            y += dy
            count += 1
        return count

    def is_won(self, x, current_player) -> bool:
        # Directions to check: horizontal, vertical, diagonals
        directions = [((0, 1), (0, -1)),  # Horizontal
                    ((1, 0), (-1, 0)),  # Vertical
                    ((1, 1), (-1, -1)),  # Main diagonal
                    ((1, -1), (-1, 1))]  # Anti-diagonal
        
        # Ensure the starting y-coordinate is valid
        y = self.y_coords[x] + 1# Get the correct y for the column
        if y is None:  # Handle case where there's no valid piece in this column
            return False

        # Check all directions
        for (dy1, dx1), (dy2, dx2) in directions:
            total = (self.count_in_direction(current_player, dx1, dy1, x, y) +
                    self.count_in_direction(current_player, dx2, dy2, x, y) + 1)  # +1 for the initial piece
            if total >= 4:
                return True
        return False
        

    def is_tie(self) -> bool:
        return self.is_board_full() and not any(self.is_won(x, p) for x in range(self.board_width) for p in ["X", "O"])

    def get_possible_moves(self, current_player):
        possible_boards = []

        for i in range(self.board_width):
            if self.is_legal_move(i):
                new_board = deepcopy(self)
                new_board.make_move(i, current_player)
                possible_boards.append(new_board)
        return possible_boards