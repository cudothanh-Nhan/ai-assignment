class Glass:
    capacity: int
    stack: list[int]

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.stack = list[int]()

    @staticmethod
    def create_glass(balls: list[int], cap: int = 4) -> 'Glass':
        glass = Glass(cap)
        glass.push_list_of_balls(balls)
        return glass

    def push_list_of_balls(self, balls: list[int]) -> bool:
        if len(balls) + len(self.stack) > self.capacity:
            return False
        for ball in balls:
            self.push_ball(ball)
        return True

    def push_ball(self, ball: int) -> None:
        self.stack.append(ball)

    def pop_ball(self) -> int:
        return self.stack.pop()

    def get_top_ball(self) -> int:
        return self.stack[-1]

    def get_all_balls(self) -> list[int]:
        return self.stack

    def is_full(self) -> bool:
        return len(self.stack) == self.capacity

    def is_empty(self) -> bool:
        return len(self.stack) == 0

    def has_single_color(self) -> bool:
        for i in range(1, len(self.stack)):
            if self.stack[i-1] != self.stack[i]:
                return False
        return True

    def get_size(self) -> int:
        return len(self.stack)

    def to_string(self) -> str:
        return ",".join([str(x) for x in self.stack])
