import pygame
from watersort.algorithm.blindsearch.solver import BFSsolver
from watersort.board import Board
from watersort.glass import Glass

from watersort.watersortUI import WatersortUI
from watersort.watersortRound import WatersortRound


class WatersortGame:
    def __init__(self, round_number):
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.game_round = WatersortRound(round_number)
        self.game_ui = WatersortUI(self.game_round)

        boardJson = self.game_round.getBoard() #import board from game_round
        boardList = list()
        for glassJson in boardJson:
            glass = Glass.create_glass(glassJson)
            boardList.append(glass)

        self.board = Board(boardList)

    def run_game_bfs_algo(self):
        self.game_ui.draw_waiting_screen()
        pygame.display.flip()
        
        algorithm = BFSsolver(self.board)
        if algorithm["isSolved"]:
            print("solved")
            moves = algorithm["moves"]
            time = algorithm["time"]
            print("elapsed time: " + str(time) + "s")
            self.simulate_solution(moves)
        else:
            print("failed")
            self.simulate_solution([], [])

    
    def simulate_solution(self, moves):
        self.game_ui.draw_board(self.board)
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
                        # TODO
                        print("move from " +str(next_move._from) + " to " + str(next_move._to))
                        self.board.move_ball(next_move)
                        
                        self.game_ui.draw_board(self.board)
                    else:
                        pygame.quit()
                        self.running = False
            if self.running:
                pygame.display.flip()
