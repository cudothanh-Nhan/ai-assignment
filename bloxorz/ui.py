from functools import reduce

import pygame
import pygame.freetype

from bloxorz.config import ui_config
from bloxorz.gameround import GameRound


class UI:
    def __init__(self, game_round):
        self.background_color = ui_config['background_color']
        self.text_area_height = ui_config['text_area_height']
        self.line_width = ui_config['line_width']
        self.window_height = ui_config['w_height']
        self.window_width = ui_config['w_width']

        self.surface = pygame.display.set_mode((self.window_width, self.window_height))
        self.surface.fill(self.background_color)

        self.window_x_mid = self.window_width / 2
        self.window_y_mid = (self.window_height - self.text_area_height) / 2

        self.game_round = game_round
        self.state = self.game_round.get_start_state()

        self.map_height = self.window_height - self.text_area_height
        self.map_width = self.window_width

        # drawing
        self.tile_size = min(self.map_height / self.game_round.height, self.map_width / self.game_round.width)
        self.map_start_x = self.window_x_mid - self.game_round.width / 2 * self.tile_size
        self.map_start_y = self.window_y_mid - self.game_round.height / 2 * self.tile_size
        self.map_end_x = self.window_x_mid + self.game_round.width / 2 * self.tile_size
        self.map_end_y = self.window_y_mid + self.game_round.height / 2 * self.tile_size

        self.unavailable_color = ui_config['unavailable_color']
        self.normal_tile_color = ui_config['normal_tile_color']
        self.soft_tile_color = ui_config['soft_tile_color']
        self.switch_rigid_color = ui_config['switch_rigid_color']
        self.switch_soft_color = ui_config['switch_soft_color']
        self.bridge_color = ui_config['bridge_color']
        self.block_color = ui_config['block_color']
        self.goal_color = ui_config['goal_color']
        self.line_color = ui_config['line_color']

        self.font = pygame.font.Font(None, 50)

    def draw_map(self, state, caption_text = 'This is a caption'):
        self.surface.fill(self.background_color)
        self.draw_grid()
        self.draw_tiles()
        self.draw_switch()
        self.draw_hole_goal()
        self.draw_caption(caption_text)
        self.draw_bridges(state.bridges)
        self.draw_block(state)

    def draw_bridges(self, bridges):
        for b in bridges:
            for t in b.tiles:
                self.draw_single_tile(t[0], t[1], self.bridge_color)

    def draw_grid(self):

        for i in range(self.game_round.width + 1):
            start_line = (self.map_start_x + i * self.tile_size, self.map_start_y)
            end_line = (self.map_start_x+ i * self.tile_size, self.map_end_y)
            pygame.draw.line(self.surface, self.line_color, start_line, end_line, self.line_width)

        for i in range(self.game_round.height + 1):
            start_line = (self.map_start_x, self.map_start_y + i * self.tile_size)
            end_line = (self.map_end_x, self.map_start_y + i * self.tile_size)
            pygame.draw.line(self.surface, self.line_color, start_line, end_line, self.line_width)

    def draw_tiles(self):
        switch_pos = list(map(lambda x: x.pos, self.game_round.bridges))
        for x in range(self.game_round.width):
            for y in range(self.game_round.height):
                if self.game_round.map[x][y] == GameRound.RIGID_TILE:
                    self.draw_single_tile(x, y, self.normal_tile_color)
                elif self.game_round.map[x][y] == GameRound.SOFT_TILE:
                    self.draw_single_tile(x, y, self.soft_tile_color)
                else:
                    self.draw_single_tile(x, y, self.unavailable_color)
    def draw_switch(self):
        for sw in self.game_round.bridges:
            self.draw_single_circle(sw.pos[0], sw.pos[1], self.switch_rigid_color if sw.is_rigid else self.switch_soft_color)
    def draw_single_tile(self, x, y, color):
        tile_start_x = self.map_start_x + x * self.tile_size + self.line_width
        tile_start_y = self.map_start_y + y * self.tile_size + self.line_width
        tile_size = self.tile_size - self.line_width

        pygame.draw.rect(self.surface, color, (tile_start_x, tile_start_y, tile_size, tile_size))

    def draw_single_circle(self, x, y, color):
        center_x = self.map_start_x + x * self.tile_size + self.tile_size / 2
        center_y = self.map_start_y + y * self.tile_size + self.tile_size / 2

        pygame.draw.circle(self.surface, color, (center_x, center_y), self.tile_size / 2)

    def draw_block(self, state):
        self.draw_single_tile(state.head[0], state.head[1], self.block_color)
        self.draw_single_tile(state.tail[0], state.tail[1], self.block_color)

    def draw_caption(self, caption_text):
        text = self.font.render(caption_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.window_width / 2, self.window_height - self.text_area_height / 2))
        self.surface.blit(text, text_rect)

    def draw_hole_goal(self):
        x = self.game_round.end[0]
        y = self.game_round.end[1]
        self.draw_single_tile(x, y, self.goal_color)

    def draw_waiting_screen(self):
        text = self.font.render('Algorithm is running...', True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.window_width / 2, self.window_height / 2))
        self.surface.blit(text, text_rect)



