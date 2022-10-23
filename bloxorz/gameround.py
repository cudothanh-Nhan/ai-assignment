import json
import math

import numpy as np

from bloxorz.blockstate import BlockState, Move

class Bridge:
    def __init__(self):
        self.pos = None
        self.tiles = []
        self.is_rigid = True
        self.is_start_trigger = False

    def __eq__(self, other):
        if not isinstance(other, Bridge):
            return False

        return other.pos == self.pos or other.tiles == self.tiles

    def __ne__(self, other):
        if not isinstance(other, Bridge):
            return True

        return not self.__eq__(other)

class GameRound:
    EMPTY = 0
    RIGID_TILE = 1
    SOFT_TILE = 2
    BRIDGE = 3
    distance_cache = {}
    def __init__(self, round_name):
        round_file = open('bloxorz/rounds/{}.json'.format(round_name), 'r')
        jsonObj = json.loads(round_file.read())

        self.map =  np.asarray(jsonObj['map']).T

        self.height = jsonObj['size']['height']
        self.width = jsonObj['size']['width']

        self.start = (jsonObj['start'][0], jsonObj['start'][1])

        self.end = (jsonObj['end'][0], jsonObj['end'][1])
        self.bridges = []
        for b in jsonObj['bridges']:
            bridge = Bridge()
            bridge.pos = b['pos']
            bridge.tiles = b['tiles']
            bridge.is_rigid = b['is_rigid']
            bridge.is_start_trigger = b['is_start_trigger']

            self.bridges.append(bridge)



    def get_start_state(self):
        head = tail = (self.start[0], self.start[1])
        bridges = list(filter(lambda x: x.is_start_trigger, self.bridges))
        return BlockState(head, tail, bridges)

    def get_next_valid_states(self, state):
        valid_states = []
        for m in Move:
            new_state =  self.calc_new_state(state, m)
            if new_state is not None:
                valid_states.append((m, new_state))

        return valid_states
    
    def calc_new_state(self, state, move):
        new_head = None
        new_tail = None

        if state.is_vertical():
            x = state.head[0]
            y = state.head[1]
            if move == Move.UP:
                new_head = (x, y - 2)
                new_tail = (x, y - 1)
            elif move == Move.DOWN:
                new_head = (x, y + 1)
                new_tail = (x, y + 2)
            elif move == Move.LEFT:
                new_head = (x - 1, y)
                new_tail = (x - 2, y)
            elif move == Move.RIGHT:
                new_head = (x + 2, y)
                new_tail = (x + 1, y)

        else:
            x1 = state.head[0]
            y1 = state.head[1]
            x2 = state.tail[0]
            y2 = state.tail[1]

            #Horizontal on y axis
            if x1 == x2:
                # UP
                if move == Move.UP:
                    new_head = new_tail = (x1, y1 - 1)
                elif move == Move.DOWN:
                    new_head = new_tail = (x2, y2 + 1)
                elif move == Move.LEFT:
                    new_head = (x1 - 1, y1)
                    new_tail = (x2 - 1, y2)
                elif move == Move.RIGHT:
                    new_head = (x1 + 1, y1)
                    new_tail = (x2 + 1, y2)

            # Horizontal on x axis.
            else:
                if move == Move.UP:
                    new_head = (x1, y1 - 1)
                    new_tail = (x2, y2 - 1)
                elif move == Move.DOWN:
                    new_head = (x1, y1 + 1)
                    new_tail = (x2, y2 + 1)
                elif move == Move.LEFT:
                    new_head = new_tail = (x2 - 1, y1)
                elif move == Move.RIGHT:
                    new_head = new_tail = (x1 + 1, y2)

        # Temporary set empty bridge
        new_state = BlockState(new_head, new_tail, [])

        if self.is_out_of_range(new_state):
            return None

        new_state.bridges = self.calc_new_bridges(new_state, state.bridges)
        if self.is_valid_state(new_state):
            return new_state
        else:
            return None
    def calc_new_bridges(self, new_state, old_bridges):
        new_bridges = old_bridges.copy()

        triggerd_bridges = self.get_trigger_bridges(new_state)
        for b in triggerd_bridges:
            if b not in old_bridges:
                new_bridges.append(b)
            else:
                new_bridges = list(filter(lambda x: x != b, new_bridges))

        return new_bridges

    def get_trigger_bridges(self, state):
        head_iter = next(filter(lambda b: [state.head[0], state.head[1]] == b.pos, self.bridges), None)
        tail_iter = next(filter(lambda b: [state.tail[0], state.tail[1]] == b.pos, self.bridges), None)
        if state.head == state.tail and \
                head_iter is not None and tail_iter is not None and \
                head_iter.is_rigid:
            return [head_iter]

        arr = []
        if head_iter is not None and not head_iter.is_rigid:
            arr.append(head_iter)

        if tail_iter is not None and tail_iter != head_iter and not tail_iter.is_rigid:
            arr.append(tail_iter)

        return arr
    def is_valid_state(self, state):

        b1 = self.is_not_out_of_edge(state)
        b2 = self.is_not_vertical_on_soft(state)

        return b1 and b2

    def is_not_vertical_on_soft(self, state):
        if state.head == state.tail and self.map[state.head[0]][state.head[1]] == GameRound.SOFT_TILE:
            return False
        else:
            return True

    def is_not_out_of_edge(self, state):
        head = state.head
        tail = state.tail

        return (self.map[head[0]][head[1]] != GameRound.EMPTY or self.is_on_bridge(head, state.bridges)) \
               and (self.map[tail[0]][tail[1]] != GameRound.EMPTY or self.is_on_bridge(tail, state.bridges))
    def is_out_of_range(self, state):
        is_in_range =  0 <= state.head[0] < self.width and \
                       0 <= state.head[1] < self.height and \
                       0 <= state.tail[0] < self.width and \
                       0 <= state.tail[1] < self.height
        return not is_in_range

    def is_reach_goal(self, state):
        head = tail = (self.end[0], self.end[1])
        return state == BlockState(head, tail, [])

    def estimate_move_num(self, source, dest, visited = []):
        try:
            visited.append(source)
            if source == dest:
                return 0
            elif GameRound.coord_to_str(source)  in GameRound.distance_cache:
                return GameRound.distance_cache[GameRound.coord_to_str(source)]

            next_coords = []
            x = source[0]
            y = source[1]


            if y - 1 >= 0 and self.is_coord_possible((x, y - 1)) and (x, y - 1) not in visited:
                next_coords.append((x, y - 1))
            if y + 1 < self.height and self.is_coord_possible((x, y + 1)) and (x, y + 1) not in visited:
                next_coords.append((x, y + 1))
            if x - 1 >= 0 and self.is_coord_possible((x - 1, y)) and (x - 1, y) not in visited:
                next_coords.append((x - 1, y))
            if x + 1 < self.width and self.is_coord_possible((x + 1, y)) and (x + 1, y) not in visited:
                next_coords.append((x + 1, y))

            min_dist = math.inf
            for c in next_coords:
                next_dist = self.estimate_move_num(c, dest, visited)
                if next_dist != math.inf:
                    GameRound.distance_cache[GameRound.coord_to_str(c)] = next_dist
                min_dist = min(1 + next_dist, min_dist)

            return min_dist
        finally:
            if len(visited) != 0:
                visited.pop()
    def is_coord_possible(self, coord):
        x = coord[0]
        y = coord[1]
        return self.map[x][y] or GameRound.is_on_bridge(coord, self.bridges)
    @staticmethod
    def is_on_bridge(coord, bridges):
        iter = filter(lambda b: [coord[0], coord[1]] in b.tiles, bridges)
        return next(iter, None) is not None

    @staticmethod
    def coord_to_str(coord):
        return '{}-{}'.format(coord[0], coord[1])