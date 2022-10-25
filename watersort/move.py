class Move:
    _from: int
    _to: int

    def __init__(self, _from: int, _to: int):
        self._from = _from
        self._to = _to
    def invert(self):
        return Move(self._to, self._from)