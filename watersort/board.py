import copy
from watersort.move import Move

class Board:
    def __init__(self, glasses_list):
        self.glasses_list = glasses_list
        self.num_of_colors = self.calc_colors_required()
    
    def get_glasses_list(self):
        return self.glasses_list
    
    def get_glass_by_index(self, index: int):
        return self.glasses_list[index]

    def is_glass_complete(self, idx):
        glass = self.glasses_list[idx]
        return glass.is_full() and glass.has_single_color()
    
    def is_complete(self):
        count = 0
        for i in range(0, len(self.glasses_list)):
            if (self.is_glass_complete(i)): count += 1
        return count == self.num_of_colors
    
    def calc_colors_required(self):
        colors = set()
        for glass in self.glasses_list:
            balls = glass.get_all_balls()
            for ball in balls:
                colors.add(ball)
        return len(colors)
    
    def find_all_moveable_glass_by_index(self, to_idx):
        indexes = list()
        to_glass = self.glasses_list[to_idx]
        for from_idx, from_glass in enumerate(self.glasses_list):
            if from_idx == to_idx:
                continue
            if from_glass.is_empty():
                continue
            if to_glass.is_empty() or from_glass.get_top_ball() == to_glass.get_top_ball():
                indexes.append(from_idx)
        return indexes
    
    def calc_all_potential_moves(self):
        moves = list()
        for to_idx, to_glass in enumerate(self.glasses_list):
            if to_glass.is_full():
                continue
            from_indexes = self.find_all_moveable_glass_by_index(to_idx)
            for from_idx in from_indexes:
                moves.append(Move(from_idx, to_idx))
        return moves
    
    def move_ball(self, move):
        ball_to_move = self.glasses_list[move._from].pop_ball()
        self.glasses_list[move._to].push_ball(ball_to_move)
    
    def clone(self):
        return copy.deepcopy(self)