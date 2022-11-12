from bloxorz.algorithm.generic import Individual
from bloxorz.blockstate import Move
from bloxorz.bloxorz_game import BloxorzGame
import argparse

from watersort.test.test_main import TestMain
from watersort.watersort_game import WatersortGame
from watersort.algorithm.astar.AStar import rounds, AStar
import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Add an argument
    parser.add_argument('--algo', type=str, default='generic',
                        help="Algorithm to solve puzzle. Enter 'manual' to play")
    parser.add_argument('--game', type=str,
                        default='bloxorz', help='Game name')
    parser.add_argument('--round', type=int, default=1, help='Game round')
    parser.add_argument('--timeout', type=int, default=20,
                        help='Algorithm timeout in second')

    args = parser.parse_args()
    print(args)

    if args.game.lower() == 'bloxorz':
        bloxorz_game = BloxorzGame(args.round)
        if args.algo.lower() == 'manual':
            bloxorz_game.run_game_manually()
        elif args.algo.lower() == 'generic':
            bloxorz_game.run_game_generic_algo(args.timeout)
        elif args.algo.lower() == 'dfs':
            bloxorz_game.run_game_dfs_algo(args.timeout)
        else:
            print('Invalid algorithm name')
    elif args.game.lower() == 'watersort':
        # watersortTest = TestMain()
        # watersortTest.test_can_create_multiple_glass()
        
        if args.algo.lower() == 'bfs':
            watersort_game = WatersortGame(args.round)
            watersort_game.run_game_bfs_algo(args.timeout)
        elif args.algo.lower() == "a*":
            if args.round > 5:
                print("Round number out of range")
            else:
                start = time.time()
                astar_game = AStar(args.round)
                astar_game.solve()
                end = time.time()
                print(end - start)
        else:
            print('Invalid algorithm name')
    else:
        print("Invalid game name. Please enter 'bloxorz' or 'watersort'")
