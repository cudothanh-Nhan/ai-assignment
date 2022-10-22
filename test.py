from bloxorz.algorithm.blind_search import BlindSearchAlgorithm


def main():
    algorithm = BlindSearchAlgorithm(game_round=3, timeout_secs=30)
    algorithm.run()
    if algorithm.found_solution():
        print(algorithm.get_solution())
    else:
        print("failed")


main()
