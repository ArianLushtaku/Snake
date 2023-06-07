import pygame
from pygame.math import Vector2
import random
from pygame import mixer


from enum import Enum

class GameState(Enum):
    MENU = 0   
    PLAYING = 1


pygame.init()
#music
mixer.init()
mixer.music.load('Graphics/snakemusic.mp3')
mixer.music.set_volume(0.3)
mixer.music.play()     

cell_size = 40
cell_number = 20

w = cell_number * cell_size
h = cell_number * cell_size
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Snake")

# Create a clock
clock = pygame.time.Clock()

# Snake
class SNAKE:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False
        self.snake = pygame.transform.scale(pygame.image.load('Graphics/apple.png').convert_alpha(), (cell_size, cell_size))
        
        self.head_up = pygame.transform.scale(pygame.image.load('Graphics/head_up.png').convert_alpha(), (cell_size, cell_size))
        self.head_down = pygame.transform.scale(pygame.image.load('Graphics/head_down.png').convert_alpha(), (cell_size, cell_size))
        self.head_left = pygame.transform.scale(pygame.image.load('Graphics/head_left.png').convert_alpha(), (cell_size, cell_size))
        self.head_right = pygame.transform.scale(pygame.image.load('Graphics/head_right.png').convert_alpha(), (cell_size, cell_size))
        
        self.tail_up = pygame.transform.scale(pygame.image.load('Graphics/tail_up.png').convert_alpha(), (cell_size, cell_size))
        self.tail_down = pygame.transform.scale(pygame.image.load('Graphics/tail_down.png').convert_alpha(), (cell_size, cell_size))
        self.tail_left = pygame.transform.scale(pygame.image.load('Graphics/tail_left.png').convert_alpha(), (cell_size, cell_size))
        self.tail_right = pygame.transform.scale(pygame.image.load('Graphics/tail_right.png').convert_alpha(), (cell_size, cell_size))
        
        self.body_vertical = pygame.transform.scale(pygame.image.load('Graphics/body_vertical.png').convert_alpha(), (cell_size, cell_size))
        self.body_horizontal = pygame.transform.scale(pygame.image.load('Graphics/body_horizontal.png').convert_alpha(), (cell_size, cell_size))
        
        self.body_bottomleft = pygame.transform.scale(pygame.image.load('Graphics/body_bottomleft.png').convert_alpha(), (cell_size, cell_size))
        self.body_bottomright = pygame.transform.scale(pygame.image.load('Graphics/body_bottomright.png').convert_alpha(), (cell_size, cell_size))
        self.body_topleft = pygame.transform.scale(pygame.image.load('Graphics/body_topleft.png').convert_alpha(), (cell_size, cell_size))
        self.body_topright = pygame.transform.scale(pygame.image.load('Graphics/body_topright.png').convert_alpha(), (cell_size, cell_size))

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(int(x_pos), int(y_pos), cell_size, cell_size)
            
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else: 
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_topleft, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bottomleft, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_topright, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_bottomright, block_rect)
            
    def update_head_graphics(self): 
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0): self.head = self.head_left
        elif head_relation == Vector2(-1, 0): self.head = self.head_right
        elif head_relation == Vector2(0, 1): self.head = self.head_up
        elif head_relation == Vector2(0, -1): self.head = self.head_down
    
    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1): self.tail = self.tail_down
        
        
        
        
        
        # for block in self.body:
        #     x_pos = int(block.x * cell_size)
        #     y_pos = int(block.y * cell_size)
        #     block_rect = pygame.Rect(int(x_pos), int(y_pos), cell_size, cell_size)
        #     #pygame.draw.rect(screen, (42, 140, 24), block_rect)
        #     screen.blit(self.snake, block_rect)

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            
            if self.body[0] in self.body[1:]:
                print("Game Over")
                main_game.reset_game()
                main_game.game_state = GameState.MENU
                return  # Exit the method to avoid further movement
                
            if self.body[0].x >= cell_number + 1:
                main_game.reset_game()
            elif self.body[0].x <= -1:
                main_game.reset_game()
            elif self.body[0].y >= cell_number + 1:
                main_game.reset_game()
            elif self.body[0].y <= -1:
                main_game.reset_game()

            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True


# Food
class FRUIT:
    def __init__(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
        self.apple = pygame.transform.scale(pygame.image.load('Graphics/apple.png').convert_alpha(), (cell_size, cell_size))


    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(self.apple, fruit_rect)
        #pygame.draw.rect(screen, (199, 55, 47), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class SCORE:
    def __init__(self):
        self.score = 0
        self.draw_score()

    def increaseScore(self, value):
        self.score += value
        self.draw_score()

    def draw_score(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        self.text = font.render(("Score: " + str(self.score)), True, pygame.Color('blue'))
        self.textRect = self.text.get_rect()
        screen.blit(self.text, self.textRect)
        
class Button:
    def __init__(self, x, y, width, height, text, bg_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.highlighted = False
        self.font = pygame.font.Font("freesansbold.ttf", 24)

    def draw(self, surface):
        button_color = self.bg_color
        outline_color = pygame.Color('black')
        outline_thickness = 3 if self.highlighted else 1

        pygame.draw.rect(surface, button_color, self.rect)
        pygame.draw.rect(surface, outline_color, self.rect, outline_thickness)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)



class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruits = []
        for i in range(1, 20):
            fruit = FRUIT()
            self.fruits.append(fruit)
        self.score = SCORE()
        self.game_state = GameState.MENU
        self.start_button = Button(
    w // 2 - 75, h // 2 -100, 150, 50, "Start",
    (0, 255, 0), (255, 255, 255) )
        self.quit_button = Button(
    w // 2 - 75, h // 2 + 25, 150, 50, "Quit",
    (0, 255, 0), (255, 255, 255) )
        self.highlighted_button = self.start_button



    def update(self):
        self.check_gamestate()
        self.snake.move_snake()
        self.check_collision()

    def draw_elements(self):
        match self.game_state:
            case GameState.MENU:
                main_game.start_button.draw(screen)
                main_game.quit_button.draw(screen)
            case GameState.PLAYING:
                for self.fruit in self.fruits:
                    self.fruit.draw_fruit()
                self.snake.draw_snake()
                self.score.draw_score()

    def check_collision(self):
        for self.fruit in self.fruits:
            if self.fruit.pos == self.snake.body[0]:
                self.fruit.randomize()
                self.snake.add_block()
                self.score.increaseScore(10)

    def reset_game(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.score = SCORE()
    
    def check_gamestate(self):
        if self.game_state == GameState.MENU:
            for button in [self.start_button, self.quit_button]:
                if button == self.highlighted_button:
                    button.highlighted = True
                else:
                    button.highlighted = False
                button.draw(screen)
                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    self.highlighted_button = self.start_button
                elif keys[pygame.K_DOWN]:
                    self.highlighted_button = self.quit_button
                elif keys[pygame.K_RETURN]:
                    if self.highlighted_button == self.start_button:
                        main_game.reset_game()
                        main_game.game_state = GameState.PLAYING
                    elif self.highlighted_button == self.quit_button:
                        exit()

# Game Loop
main_game = MAIN()
SCREEN_UPDATE = pygame.USEREVENT

SCREEN_DELAY = 150
pygame.time.set_timer(SCREEN_UPDATE, SCREEN_DELAY)
key_delay = 50
last_key_time = pygame.time.get_ticks()
screen_update_timer = pygame.time.get_ticks()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False

        if event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - last_key_time
            if elapsed_time > key_delay:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                        last_key_time = current_time
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                        last_key_time = current_time
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
                        last_key_time = current_time
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                        last_key_time = current_time

    # Update game objects
    screen.fill((175, 215, 70))
    main_game.draw_elements()


    pygame.display.flip()

    # Set framerate
    clock.tick(60)

pygame.quit()

