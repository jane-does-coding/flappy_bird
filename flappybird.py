import pygame
from sys import exit

GAME_WIDTH = 360
GAME_HEIGHT = 640

# bird class

bird_x = GAME_WIDTH/8
bird_y = GAME_HEIGHT/2
bird_width = 34
bird_height = 24

class Bird(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, bird_x, bird_y, bird_width, bird_height)
        self.img = img



# pipe class
pipe_x = GAME_WIDTH
pipe_y = 0
pipe_width = 64
pipe_height = 512

class Pipe(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, pipe_x, pipe_y, pipe_width, pipe_height)
        self.img = img
        self.passed = False


# Game images
background_image = pygame.image.load("flappybirdbg.png")
bird_image = pygame.image.load("flappybird.png")
bird_image = pygame.transform.scale(bird_image, (bird_width, bird_height))
top_pipe_image = pygame.image.load("toppipe.png")
top_pipe_image = pygame.transform.scale(top_pipe_image, (pipe_width, pipe_height))
bottom_pipe_image = pygame.image.load("bottompipe.png")
bottom_pipe_image = pygame.transform.scale(bottom_pipe_image, (pipe_width, pipe_height))

# game Logic
bird = Bird(bird_image)
pipes = []

def draw():
    window.blit(background_image, (0, 0))
    window.blit(bird.img, (bird))

    for pipe in pipes:
        window.blit(pipe.img, pipe)


def create_pipes():
    top_pipe = Pipe(top_pipe_image)
    pipes.append(top_pipe)

    print(len(pipes))

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

create_pipes_timer = pygame.USEREVENT + 0
pygame.time.set_timer(create_pipes_timer, 1500) # create a new pipe every 1.5 seconds


while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == create_pipes_timer:   
            create_pipes()

    draw()
    pygame.display.update()
    clock.tick(60) # 60 fps? Not an AI comment, I'm just learning, ok
