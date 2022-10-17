import json
import numpy as np

from bloxorz.blockstate import BlockState, Move


class GameRound:
    def __init__(self, round_name):
        round_file = open('bloxorz/rounds/{}.json'.format(round_name), 'r')
        jsonObj = json.loads(round_file.read())

        self.map =  np.asarray(jsonObj['map']).T

        self.height = jsonObj['size']['height']
        self.width = jsonObj['size']['width']

        self.start = jsonObj['start']

        self.end = jsonObj['end']

    def get_start_state(self):
        head = tail = (self.start[0], self.start[1])
        return BlockState(head, tail)

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
        new_state = BlockState(new_head, new_tail)

        if self.is_valid_state(new_state):
            return new_state
        else:
            return None

    def is_valid_state(self, state):
        return self.is_tile_available(state.head[0], state.head[1]) and\
               self.is_tile_available(state.tail[0], state.tail[1])

    def is_tile_available(self, x, y):
        return 0 <= x < self.width and \
               0 <= y < self.height and\
               self.map[x][y] == 1

    def is_reach_goal(self, state):
        head = tail = (self.end[0], self.end[1])
        return state == BlockState(head, tail)