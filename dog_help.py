import pygame
from random import randint, choice, choices
import math
import time

class Option():
    def __init__(self, initiation):
        self.gamee = initiation
        self.mid_w, self.mid_h = self.gamee.width/2, self.gamee.height/2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -80
        

        self.state = 'Start'
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.instrucx, self.instrucy = self.mid_w, self.mid_h + 50
        self.creditx, self.credity = self.mid_w, self.mid_h + 70
        self.quitx, self.quity = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def move_cursor(self):
        if self.gamee.DOWN:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.instrucx + self.offset, self.instrucy)
                self.state = 'instructions'
            elif self.state == "instructions":
                self.cursor_rect.midtop = (self.creditx + self.offset, self.credity)
                self.state = 'Credits'
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = 'quit'
            elif self.state == "quit":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            
        elif self.gamee.UP:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = 'quit'
            elif self.state == "quit":
                self.cursor_rect.midtop = (self.creditx + self.offset, self.credity)
                self.state = 'Credits'
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.instrucx + self.offset, self.instrucy)
                self.state = 'instructions'
            elif self.state == "instructions":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'

    def check_input(self):
        self.move_cursor()
        if self.gamee.START_KEY:
            if self.state == 'Start':
                self.run_display = False
                self.gamee.curr_menu = self.gamee.gameloop

            elif self.state == 'instructions':
                self.run_display = False
                self.gamee.curr_menu = self.gamee.instructions
        
            elif self.state == 'Credits':
                count = 0 
                while count < 1:
                    self.gamee.window.fill((25, 25, 25))
                    self.gamee.draw_text('The game is created by Elia', 30, self.gamee.width/2, self.gamee.height/2)
                    pygame.display.update()
                    time.sleep(3)
                    count += 1
                # self.gamee.curr_menu = self.gamee.credits
                # self.run_display = False

            elif self.state == 'quit':
                self.run_display = False
                self.gamee.running = False 

    def draw_cursor(self):
        self.gamee.draw_text('>', 15, self.cursor_rect.x, self.cursor_rect.y)
        self.gamee.START_KEY, self.gamee.END_KEY = False, False
        self.gamee.DOWN, self.gamee.UP = False, False
        pygame.display.update()

    def display(self):
        self.run_display = True
        while self.run_display:
            self.gamee.check_events()
            self.check_input()
            self.gamee.window.fill((25, 25, 25))
            self.gamee.draw_text('Main Menu', 30, self.gamee.width/2, self.gamee.height/2 - 20)
            self.gamee.draw_text('Start game', 25, self.startx, self.starty)
            self.gamee.draw_text('Instructions', 25, self.instrucx, self.instrucy)
            self.gamee.draw_text('Credits', 25, self.creditx, self.credity)
            self.gamee.draw_text('Quit', 25, self.quitx, self.quity)
            self.draw_cursor()

class Instructions(Option):
    def __init__(self, initiation):
        Option.__init__(self, initiation)
        self.state = 'back'
        self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)

    def display(self):
        self.run_display = True
        while self.run_display:
            self.gamee.check_events()
            self.check_input()
            self.gamee.window.fill((25, 25, 25))
            self.gamee.draw_text('Instructions', 30, self.gamee.width/2, self.gamee.height/2 - 20)
            self.gamee.draw_text('-Using less time as possible to help the dog find the bone', 15, self.startx, self.starty)
            self.gamee.draw_text('-Press the arrows towards the bone to increase the probability of the dog to move the direction of the bone',
                                 15, self.instrucx, self.instrucy)
            self.gamee.draw_text('-When the dog is near the bone press "Enter" to let the dog find the bone', 15, self.creditx, self.credity)
            self.gamee.draw_text('Back', 25, self.quitx, self.quity)
            self.draw_cursor()

    def check_input(self):
        if self.gamee.START_KEY:
            if self.state == 'back':
                self.run_display = False
                self.gamee.curr_menu = self.gamee.optionn

class MainGame():
    def __init__(self, initiation):
        self.gamee = initiation
        pygame.display.set_caption('Help Dog')
        self.bone = pygame.transform.scale(pygame.image.load('bone.png'), (20, 20))
        self.dog = pygame.transform.scale(pygame.image.load('dog.png'), (20, 20))

        self.target_x = randint(1, 500)
        self.target_y = self.target_x
        self.well_x = [a for a in range(self.target_x-5, self.target_x+5)]
        self.well_y = [a for a in range(self.target_x-5, self.target_y+5)]
        self.x, self.y = 250, 250
        self.count, self.dista = 0, 500
        # print(self.count)
        self.options = ["left", "right", "upp", "downn"]
        self.active_list = self.options

        self.clock = pygame.time.Clock()
        self.close_x = [a for a in range(self.target_x-50, self.target_x+50)]
        self.close_y = [b for b in range(self.target_y-50, self.target_y+50)]

    def display(self):
        self.count = 0
        start = time.time()
        while self.count <= 1000:
            self.clock.tick(100)
            pos = choice(self.active_list)
            # self.gamee.window.blit(self.wood, (0, 0))
            self.gamee.window.fill((127, 127, 127))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.count = 10000
                    self.gamee.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.active_list = self.options

                    if event.key == pygame.K_ESCAPE:
                        self.count = 10000
                        self.gamee.curr_menu = self.gamee.optionn

                    if event.key == pygame.K_LEFT:
                        left_list = choices(self.options, [.6, .1, .2, .2], k=10)
                        self.active_list = left_list
                    if event.key == pygame.K_RIGHT:
                        right_list = choices(self.options, [.1, .6, .2, .2], k=10)
                        self.active_list = right_list
                    if event.key == pygame.K_UP:
                        up_list = choices(self.options, [.2, .2, .6, .1], k=10)
                        self.active_list = up_list
                    if event.key == pygame.K_DOWN:
                        down_list = choices(self.options, [.2, .2, .1, .6], k=10)
                        self.active_list = down_list

            if pos == "left":
                self.x -= 1
            elif pos == "right":
                self.x += 1
            elif pos == "upp":
                self.y -= 1
            elif pos == "downn":
                self.y += 1

            self.gamee.window.blit(self.bone, (self.target_x, self.target_y))

            if self.x in self.close_x and self.y in self.close_y:
                # pygame.draw.rect(self.gamee.window, (0, 255, 0), (self.x, self.y, 1, 1))
                self.gamee.window.blit(self.dog, (self.x, self.y))

            else:
                # pygame.draw.rect(self.gamee.window, (255, 255, 255), (self.x, self.y, 1, 1))
                self.gamee.window.blit(self.dog, (self.x, self.y))

            # Calculating distance of the dog from the bone
            a, b = (self.x - self.target_x)**2, (self.y - self.target_y)**2
            new_dista = math.sqrt((a + b))

            # displaying the high score since started playing
            high = min(self.gamee.high_score)
            if len(self.gamee.high_score) == 1:
                self.gamee.draw_text('High Score: 0 seconds', 30, 180, 30)  
            elif len(self.gamee.high_score) >= 2:  
                self.gamee.draw_text(f'High Score: {high} seconds', 30, 180, 30)

            if new_dista < self.dista:
                self.dista = new_dista
                good_y = self.y
                good_x = self.x

            if self.x in self.well_x and self.y in self.well_y:
                the_x = randint(1, 500)
                the_y = randint(1, 500)
                self.target_x, self.target_y =  the_x, the_y 
                self.well_x = [a for a in range(self.target_x-5, self.target_x+5)]
                self.well_y = [a for a in range(self.target_y-5, self.target_y+5)]
                self.close_x = [a for a in range(self.target_x-50, self.target_x+50)]
                self.close_y = [b for b in range(self.target_y-50, self.target_y+50)]
                self.gamee.window.fill((127, 127, 127))
                self.dista = 400
                end = time.time()
                # print(end - start)
                self.gamee.high_score.append(round((end - start), 2))
                now = 0
                while now < 1:
                    self.gamee.window.fill((25, 25, 25))
                    self.gamee.draw_text(f'You used {str(round((end - start), 2))} seconds', 30, self.gamee.width/2, self.gamee.height/2 - 20)
                    pygame.display.update()
                    time.sleep(5)
                    now = 2
                start = time.time()

            if self.count == 1000:
                self.gamee.window.fill((127, 127, 127))
                self.x, self.y = good_x, good_y
                self.count = 0

            pygame.display.update()
            self.count += 1
