import pygame
from watersort.board import Board

from watersort.config import ui_config
from watersort.glass import Glass
from watersort.move import Move

class WatersortUI:
    def __init__(self, game_round):
        self.font = pygame.font.Font(None, 50)

        self.backgroundcolor = ui_config['background_color']
        self.window_height = ui_config['w_height']
        self.window_width = ui_config['w_width']
        self.glass_left = ui_config['g_left']
        self.glass_top = ui_config['g_top']
        self.glass_width = ui_config['g_width']
        self.glass_height = ui_config['g_height']
        self.ball_radius = ui_config['ball_radius']

        self.surface = pygame.display.set_mode((self.window_width, self.window_height))
        self.surface.fill(self.backgroundcolor)

        self.game_round = game_round

    def convert_int_to_color(self, num):
        if num == 1:
            return (255,0,0)
        elif num == 2:
            return (255,255,0)
        elif num == 3:
            return (0,0,255)
        elif num == 4:
            return (255,128,0)
        return (0,0,0)
    
    def draw_board(self, board: Board):
        self.surface.fill(self.backgroundcolor)
        glasses_list = board.get_glasses_list()
        for x in range(len(glasses_list)):
            width = self.glass_width
            left = self.glass_left*(x+1) + width*x
            top = self.glass_top
            height = self.glass_height
            glass = board.get_glasses_list()[x]
            self.draw_glass(glass, left, top, width, height)
    
    def draw_glass(self, glass: Glass, left: float, top: float, width: float, height: float):
        # glass = Glass([1,2,3,4]
        pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(left, top, width, height), 2)
        new_glass = glass.clone()
        capacity = new_glass.get_capacity()
        size = new_glass.get_size()
        idx = size-1
        while not new_glass.is_empty():
            ball = new_glass.pop_ball()
            x_ball = left + width/2
            y_ball = top + (-2*idx + 7)*self.ball_radius
            self.draw_ball(self.convert_int_to_color(ball), (x_ball, y_ball))
            idx -= 1
            
    def draw_ball(self, color, center):
        pygame.draw.circle(self.surface, color, center, self.ball_radius)
    
    def draw_waiting_screen(self):
        text = self.font.render('Algorithm is running...', True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.window_width / 2, self.window_height / 2))
        self.surface.blit(text, text_rect)
