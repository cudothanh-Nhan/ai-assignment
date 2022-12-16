import game



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
    board = game.convert_board(board, 2, 2, -1)
    print_board(board)

main()
