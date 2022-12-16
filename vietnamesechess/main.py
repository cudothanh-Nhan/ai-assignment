import game


if __name__ == '__main__':
    board = [
            [1,0,1,1,1],
            [1,1,0,0,1],
            [-1,0,0,1,0],
            [-1,-1,-1,0,-1],
            [-1,0,0,-1,-1]
        ]
    player = -1
    legal_move = game.get_legal_move(board, player)
    for x in legal_move:
        x.print()
