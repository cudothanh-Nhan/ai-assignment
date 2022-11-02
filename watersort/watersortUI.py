import pygame
from watersort.board import Board

from watersort.config import ui_config
from watersort.glass import Glass

class WatersortUI:
    def __init__(self, game_round):
        self.backgroundcolor = ui_config['background_color']
        self.window_height = ui_config['w_height']
        self.window_width = ui_config['w_width']

        self.surface = pygame.display.set_mode((self.window_width, self.window_height))
        self.surface.fill(self.backgroundcolor)

        self.game_round = game_round
    
    def draw_board(self, board: Board):    
        for glass in board.get_glasses_list():
            self.draw_glass(glass)
    
    def draw_glass(self, glass: Glass):
        # glass = Glass([1,2,3,4])
        cap = glass.get_size()
        pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(30,30,60,60), 2)
    
    def draw_glass(self): #for testing
        pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(30,30,60,60), 2)

    def draw_move(self, _from, _to):
        None
    
    def draw_waiting_screen(self):
        None
    
