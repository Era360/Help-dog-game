import pygame
from dog_help import *

class Game():
    def __init__(self):
        pygame.init()
        self.width, self.height = 1280, 708
        self.running = True
        self.START_KEY, self.END_KEY = False, False
        self.DOWN, self.UP = False, False
        self.high_score = [1000]

        self.window = pygame.display.set_mode((self.width, self.height))

        #####################################
        self.optionn = Option(self)
        self.gameloop = MainGame(self)
        self.instructions = Instructions(self)

        self.curr_menu = self.optionn
        ####################################

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.curr_menu.run_display = False
                self.run_display = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.curr_menu.run_display = False
                    self.run_display = False

                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.END_KEY = True
                if event.key == pygame.K_UP:
                    self.UP = True
                if event.key == pygame.K_DOWN:
                    self.DOWN = True    

    def draw_text(self, text, size, x, y, color=(255, 255, 255)):
        font = pygame.font.Font(pygame.font.get_default_font(), size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.window.blit(text_surface, text_rect)