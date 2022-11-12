import os

import pygame

from bloxorz.algorithm import GenericAlgorithm, BlindSearchAlgorithm
from bloxorz.blockstate import Move
from bloxorz.gameround import GameRound
from bloxorz.ui import UI

class BloxorzGame:
    def __init__(self, round_number):
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.game_round = GameRound(round_number)
        self.game_ui = UI(self.game_round)
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    def run_game_dfs_algo(self, timeout):
        self.game_ui.draw_waiting_screen()
        pygame.display.flip()

        algorithm = BlindSearchAlgorithm(self.game_round, timeout)
        algorithm.run()
        if algorithm.found_solution():
            print(algorithm.get_solution())
            solution = algorithm.get_solution()
            self.simulate_solution(solution, caption="Found solution with DFS")
        else:
            print("failed")
            self.simulate_solution(
                [], caption="Not found solution. Press <space> to exit")


    def run_game_generic_algo(self, timeout):
        algorithm = GenericAlgorithm(self.game_round, timeout)

        self.game_ui.draw_waiting_screen()
        pygame.display.flip()

        algorithm.run()
        solution = algorithm.get_best_move()
        # Print solution info

        print('----------- Algorithm summary -----------')
        print(algorithm)
        print('Found solution = {}'.format(algorithm.is_found))
        print('Elapsed time = {:.2f} seconds'.format(algorithm.elapsed_time))
        print('Max mem use = {:.2f} MB'.format(algorithm.max_mem_use))
        print('Num of move = {}'.format(len(solution)))
        print('Best move = {}'.format(solution))

        # Simulate solution
        state = self.game_round.get_start_state()
        caption = 'Found solution' if algorithm.is_found else 'Not found solution. Simulate best move'
        self.game_ui.draw_map(state, caption)
        self.simulate_solution(solution, caption)

    def simulate_solution(self, moves, caption):
        state = self.game_round.get_start_state()
        self.game_ui.draw_map(state, caption)
        moveit = iter(moves)
        while self.running:
            self.clock.tick(60)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    next_move = next(moveit, None)
                    if next_move is not None:
                        state = self.game_round.calc_new_state(state, next_move)
                        if state is not None:
                            if self.game_round.is_reach_goal(state):
                                self.game_ui.draw_map(state, 'End')
                            else:
                                self.game_ui.draw_map(state, caption)
                    else:
                        pygame.quit()
                        self.running = False

            if self.running:
                pygame.display.flip()

    def process_input(self, old_state, events):
        new_state = None

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_state = self.game_round.calc_new_state(old_state, Move.LEFT)
                elif event.key == pygame.K_RIGHT:
                    new_state = self.game_round.calc_new_state(old_state, Move.RIGHT)
                elif event.key == pygame.K_UP:
                    new_state = self.game_round.calc_new_state(old_state, Move.UP)
                elif event.key == pygame.K_DOWN:
                    new_state = self.game_round.calc_new_state(old_state, Move.DOWN)
            elif event.type == pygame.QUIT:
                pygame.quit()

        return new_state

    def run_game_manually(self):
        state = self.game_round.get_start_state()
        self.game_ui.draw_map(state, 'Manual mode')
        while self.running:
            self.clock.tick(60)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
                elif not self.game_round.is_reach_goal(state):
                    new_state = self.process_input(state, events)
                    if new_state is not None:
                        state = new_state
                        if self.game_round.is_reach_goal(new_state):
                            self.game_ui.draw_map(new_state, 'Reach Hole. Mission completes')
                        else:
                            self.game_ui.draw_map(new_state, 'Manual mode')

            if self.running:
                pygame.display.flip()

