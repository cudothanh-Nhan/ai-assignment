class Move:
    def __init__(self, _from, _to):
        self._from = _from
        self._to = _to
    def invert(self):
        return Move(self._to, self._from)