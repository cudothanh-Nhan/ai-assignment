import copy

class Move:
    from_x: int
    from_y: int
    to_x: int
    to_y: int

    def __init__(self, from_x: int, from_y: int, to_x: int, to_y: int):
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
    
    def print(self):
        _str = "(" + str(self.from_x) + ", " + str(self.from_y) + ") to (" + str(self.to_x) + ", " + str(self.to_y) + ")"
        print(_str)


def convert_board(board: list, move: Move, player: int):
    # board: [[], [], [], [], []]
    # player: 1 or -1
    new_board = copy.deepcopy(board)
    opponent = -player
    new_board[move.from_x][move.from_y] = 0
    new_board[move.to_x][move.to_y] = player

    # ganh
    if move.to_x == 0 or move.to_x == 4:
        if move.to_y == 0 or move.to_y == 4:
            return new_board
        else:
            if new_board[move.to_x][move.to_y - 1] == opponent and new_board[move.to_x][move.to_y + 1] == opponent:
                new_board[move.to_x][move.to_y - 1] = player
                new_board[move.to_x][move.to_y + 1] = player

                new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x, move.to_y - 1), player)
                new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x, move.to_y + 1), player)

    elif move.to_y == 0 or move.to_y == 4:
        if new_board[move.to_x - 1][move.to_y] == opponent and new_board[move.to_x + 1][move.to_y] == opponent:
            new_board[move.to_x - 1][move.to_y] = player
            new_board[move.to_x + 1][move.to_y] = player

            new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x - 1, move.to_y), player)
            new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x + 1, move.to_y), player)
    else:
        if new_board[move.to_x][move.to_y - 1] == opponent and new_board[move.to_x][move.to_y + 1] == opponent:
            new_board[move.to_x][move.to_y - 1] = player
            new_board[move.to_x][move.to_y + 1] = player

            new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x, move.to_y - 1), player)
            new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x, move.to_y + 1), player)

        if new_board[move.to_x - 1][move.to_y] == opponent and new_board[move.to_x + 1][move.to_y] == opponent:
            new_board[move.to_x - 1][move.to_y] = player
            new_board[move.to_x + 1][move.to_y] = player

            new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x - 1, move.to_y), player)
            new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x + 1, move.to_y), player)
        if (new_board[move.to_x - 1][move.to_y - 1] == opponent and new_board[move.to_x + 1][
            move.to_y + 1] == opponent):
            new_board[move.to_x - 1][move.to_y - 1] = player
            new_board[move.to_x + 1][move.to_y + 1] = player

            new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x - 1, move.to_y - 1), player)
            new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x + 1, move.to_y + 1), player)
        if (new_board[move.to_x + 1][move.to_y - 1] == opponent and new_board[move.to_x - 1][
            move.to_y + 1] == opponent):
            new_board[move.to_x + 1][move.to_y - 1] = player
            new_board[move.to_x - 1][move.to_y + 1] = player

            new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x + 1, move.to_y - 1), player)
            new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x - 1, move.to_y + 1), player)

    # vay/chet

    return new_board

def is_valid_move(board, move: Move) -> bool:
    if move.to_x <0 or move.to_x>4 or move.to_y<0 or move.to_y>4 or not move.to_x - move.from_x in [-1, 0, 1] or not move.to_y - move.from_y in [-1,0,1]:
        return False
    if board[move.to_x][move.to_y] != 0:
        return False
    return True

def get_legal_move(board, player: int) -> list[Move]:
    legal_move = list()
    for row_idx, row in enumerate(board):
        for col_idx, col in enumerate(row):
            if col == player:
                lst = list()
                if (row_idx + col_idx) %2 == 0:
                    lst = [Move(row_idx, col_idx, row_idx-1, col_idx-1), Move(row_idx, col_idx, row_idx-1, col_idx), Move(row_idx, col_idx, row_idx-1, col_idx+1), Move(row_idx, col_idx, row_idx, col_idx-1), Move(row_idx, col_idx, row_idx, col_idx+1), Move(row_idx, col_idx, row_idx+1,col_idx-1), Move(row_idx, col_idx, row_idx+1, col_idx), Move(row_idx, col_idx, row_idx+1, col_idx+1)]
                else:
                    lst = [Move(row_idx, col_idx, row_idx-1, col_idx), Move(row_idx, col_idx, row_idx, col_idx-1), Move(row_idx, col_idx, row_idx, col_idx+1), Move(row_idx, col_idx, row_idx+1, col_idx)] 
                for x in lst:
                    if is_valid_move(board, x):
                        legal_move.append(x)
    return legal_move


def print_board(board):
    for i in board:
        row_str = ''
        for j in i:
            row_str += str(j).rjust(4)
        print(row_str)