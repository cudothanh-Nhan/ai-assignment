import copy

class Move:
    from_x: int
    from_y: int
    to_x: int
    to_y: int

    def __init__(self, from_x: int, from_y: int, to_x: int, to_y: int):
        self.from_x = from_x
        self.from_y = from_y
        self.to_x =to_x 
        self.to_y = to_y
        
def convert_board(board: list, move: Move, player: int):
    # board: [[], [], [], [], []]
    # player: 1 or -1
    new_board = copy.deepcopy(board)
    opponent = -player
    new_board[move.from_x][move.from_y] = 0
    new_board[move.to_x][move.to_y] = player

    #ganh
    if(move.to_x == 0 or move.to_x == 4):
        if (move.to_y == 0 or move.to_y == 4):
            return new_board
        else:
            if(new_board[move.to_x][move.to_y - 1] == opponent and new_board[move.to_x][move.to_y + 1] == opponent):
                new_board[move.to_x][move.to_y - 1] = player
                new_board[move.to_x][move.to_y + 1] = player
                

                new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x, move.to_y - 1), player)
                new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x, move.to_y + 1), player)

    elif(move.to_y == 0 or move.to_y == 4):
        if(new_board[move.to_x - 1][move.to_y] == opponent and new_board[move.to_x + 1][move.to_y] == opponent):
            new_board[move.to_x - 1][move.to_y] = player
            new_board[move.to_x + 1][move.to_y] = player

            new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x - 1, move.to_y), player)
            new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x + 1, move.to_y), player)
    else:
        if(new_board[move.to_x][move.to_y - 1] == opponent and new_board[move.to_x][move.to_y + 1] == opponent):
            new_board[move.to_x][move.to_y - 1] = player
            new_board[move.to_x][move.to_y + 1] = player

            new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x, move.to_y - 1), player)
            new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x, move.to_y + 1), player)

        if(new_board[move.to_x - 1][move.to_y] == opponent and new_board[move.to_x + 1][move.to_y] == opponent):
            new_board[move.to_x - 1][move.to_y] = player
            new_board[move.to_x + 1][move.to_y] = player

            new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x-1, move.to_y), player)
            new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x+1, move.to_y), player)
        if(new_board[move.to_x - 1][move.to_y - 1] == opponent and new_board[move.to_x + 1][move.to_y + 1] == opponent):
            new_board[move.to_x - 1][move.to_y - 1] = player
            new_board[move.to_x + 1][move.to_y + 1] = player

            new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x-1, move.to_y - 1), player)
            new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x+1, move.to_y + 1), player)
        if(new_board[move.to_x + 1][move.to_y - 1] == opponent and new_board[move.to_x - 1][move.to_y + 1] == opponent):
            new_board[move.to_x + 1][move.to_y - 1] = player
            new_board[move.to_x - 1][move.to_y + 1] = player

            new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x+1, move.to_y - 1), player)
            new_board = convert_board(new_board, Move(move.from_x, move.from_y, move.to_x-1, move.to_y + 1), player)
    
    # vay/chet



    return new_board

def print_board(board):
    print("Board is: ")
    print(board)


def main():
    board = [
        [0,0,0,0,0],
        [0,1,-1,1,0],
        [1,1,0,1,0],
        [0,1,0,1,0],
        [0,0,0,0,0]
    ]
    board = convert_board(board, 2, 2, -1)
    print_board(board)

main()
