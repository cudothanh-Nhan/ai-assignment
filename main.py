from bloxorz.bloxorz_game import BloxorzGame
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Add an argument
    parser.add_argument('--algo', type=str, default='generic', help="Algorithm to solve puzzle. Enter 'manual' to play")
    parser.add_argument('--game', type=str, default='bloxorz', help='Game name')
    parser.add_argument('--round', type=int, default=1, help='Game round')
    parser.add_argument('--timeout', type=int, default=20, help='Algorithm timeout in second')

    args = parser.parse_args()
    print(args)

    if args.game.lower() == 'bloxorz':
        bloxorz_game = BloxorzGame(args.round)
        if args.algo.lower() == 'manual':
            bloxorz_game.run_game_manually()
        elif args.algo.lower() == 'generic':
            bloxorz_game.run_game_generic_algo(args.timeout)
        else:
            print('Invalid algorithm name')
    else:
        print("Invalid game name. Please enter 'bloxorz' or 'water_puzzle'")
