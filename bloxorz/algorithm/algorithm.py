from bloxorz.blockstate import Move


class Algorithm:
    def __init__(self, game_round, timeout):
        raise NotImplementedError("error: required method '__init__'")

    def run(self):
        raise NotImplementedError("error: required method 'run'")

    def found_solution(self):
        raise NotImplementedError("error: required method 'found_solution'")

    def get_solution(self) -> list(Move):
        raise NotImplementedError("error: required method 'get_solution'")
