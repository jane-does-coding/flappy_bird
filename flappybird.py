import pygame
from sys import exit
import random

GAME_WIDTH = 360
GAME_HEIGHT = 640

#bird 
bird_x = GAME_WIDTH/8
bird_y = GAME_HEIGHT/2
bird_width = 34
bird_height = 24

class Bird(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, bird_x, bird_y, bird_width, bird_height)
        self.img = img

#pipe
pipe_x = GAME_WIDTH
pipe_y = 0
pipe_width = 64
pipe_height = 512

class Pipe(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, pipe_x, pipe_y, pipe_width, pipe_height)
        self.img = img
        self.passed = False

#images
background_image = pygame.image.load("flappybirdbg.png") 
bird_image = pygame.image.load("flappybird.png")
bird_image = pygame.transform.scale(bird_image, (bird_width, bird_height))
top_pipe_image = pygame.image.load("toppipe.png")
top_pipe_image = pygame.transform.scale(top_pipe_image, (pipe_width, pipe_height))
bottom_pipe_image = pygame.image.load("bottompipe.png")
bottom_pipe_image = pygame.transform.scale(bottom_pipe_image, (pipe_width, pipe_height))
apple_image = pygame.image.load("apple.png")
apple_image = pygame.transform.scale(apple_image, (30, 30))

# power ups
powerups = []
invincible = False
invincible_start = 0
invincible_duration = 3000 

class PowerUp(pygame.Rect):
    def __init__(self, img, x, y):
        pygame.Rect.__init__(self, x, y, 30, 30)
        self.img = img

#game logic
bird = Bird(bird_image)
pipes = []
velocity_x = -2 
velocity_y = 0
gravity = 0.4
score = 0
game_over = False

def draw():
    window.blit(background_image, (0, 0))

    if invincible:
        temp = bird.img.copy()
        temp.set_alpha(120)
        window.blit(temp, bird)
    else:
        window.blit(bird.img, bird)

    for pipe in pipes:
        window.blit(pipe.img, pipe)

    # Power-ups
    for powerup in powerups:
        window.blit(powerup.img, powerup)

    text_font = pygame.font.SysFont("Comic Sans MS", 45)
    text_render = text_font.render(str(int(score)), True, "white")
    window.blit(text_render, (5, 0))

    # Timer LAST so it draws on top
    if invincible:
        elapsed = pygame.time.get_ticks() - invincible_start
        remaining = max(0, (invincible_duration - elapsed) / 1000)
        timer_font = pygame.font.SysFont("Comic Sans MS", 30)
        timer_render = timer_font.render(f"{remaining:.1f}", True, "yellow")
        timer_rect = timer_render.get_rect(topright=(GAME_WIDTH - 5, 5))
        window.blit(timer_render, timer_rect)


def move():
    global velocity_y, score, game_over, invincible, invincible_start

    velocity_y += gravity
    bird.y += velocity_y
    bird.y = max(bird.y, 0) 

    if bird.y > GAME_HEIGHT:
        game_over = True
        return

    for pipe in pipes:
        pipe.x += velocity_x

        if not pipe.passed and bird.x > pipe.x + pipe.width:
            score += 0.5
            pipe.passed = True
        
        if bird.colliderect(pipe) and not invincible:
            game_over = True
            return
        
    # powerups
    for powerup in powerups[:]:
        powerup.x += velocity_x

        if bird.colliderect(powerup):
            invincible = True
            invincible_start = pygame.time.get_ticks()
            powerups.remove(powerup)

    # remove off-screen pipes
    while len(pipes) > 0 and pipes[0].x < -pipe_width:
        pipes.pop(0)

    # remove off-screen powerups
    for powerup in powerups[:]:
        if powerup.x < -50:
            powerups.remove(powerup)

    # turn off invincibility after 5 s
    if invincible:
        if pygame.time.get_ticks() - invincible_start > invincible_duration:
            invincible = False

def create_pipes():
    random_pipe_y = pipe_y - pipe_height/4 - random.random()*(pipe_height/2)
    opening_space = GAME_HEIGHT/4

    top_pipe = Pipe(top_pipe_image)
    top_pipe.y = random_pipe_y
    pipes.append(top_pipe)

    bottom_pipe = Pipe(bottom_pipe_image)
    bottom_pipe.y = top_pipe.y + top_pipe.height + opening_space
    pipes.append(bottom_pipe)

    if random.random() < 0.3:
        apple_x = pipe_x + pipe_width + 10
        apple_y = top_pipe.y + top_pipe.height + opening_space / 2
        powerups.append(PowerUp(apple_image, apple_x, apple_y))

    print(len(pipes))

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

create_pipes_timer = pygame.USEREVENT + 0
pygame.time.set_timer(create_pipes_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == create_pipes_timer and not game_over:
            create_pipes()
        
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_x, pygame.K_UP):
                velocity_y = -6

                #reset
                if game_over:
                    bird.y = bird_y
                    pipes.clear()
                    score = 0
                    game_over = False
    
    if not game_over:
        move()
        draw()
        pygame.display.update()
        clock.tick(60) 
