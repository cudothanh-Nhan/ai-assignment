import copy


class Glass:
    def __init__(self, capacity):
        self.capacity = capacity
        self.stack = list()
    
    def get_capacity(self):
        return self.capacity

    @staticmethod
    def create_glass(balls, cap = 4):
        glass = Glass(4)
        glass.push_list_of_balls(balls)
        return glass

    def push_list_of_balls(self, balls):
        if len(balls) + len(self.stack) > self.capacity:
            return False
        for ball in balls:
            self.push_ball(ball)

    def push_ball(self, ball: int):
        self.stack.append(ball)

    def pop_ball(self):
        ball = self.stack[-1]
        self.stack = self.stack[:-1]
        return ball
    
    def get_top_ball(self):
        return self.stack[-1]
    
    def get_all_balls(self):
        balls = list()
        for i in range(0, len(self.stack)):
            balls.append(self.stack[i])
        return balls

    def is_full(self):
        return len(self.stack) == self.capacity
    
    def is_empty(self):
        return len(self.stack) == 0

    def has_single_color(self):
        for i in range(1, len(self.stack)):
            if self.stack[i-1] != self.stack[i]: return False
        return True
    
    def get_size(self):
        return len(self.stack)
    
    def to_string(self):
        return ",".join([str(x) for x in self.stack])
    
    def clone(self):
        return copy.deepcopy(self)

        