import pygame
pygame.init()

SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
background_img = pygame.image.load("assets/bg.png")
base_img = pygame.image.load("assets/base.png")
base_img = pygame.transform.scale(base_img, (SCREEN_WIDTH, 112))

def move_base(base_x):
    screen.blit(base_img, (base_x, 400))
    screen.blit(base_img, (base_x + SCREEN_WIDTH, 400))


base_x = 0
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.blit(background_img, (0, 0))

    move_base(base_x)
    base_x += 1
    if base_x == -(SCREEN_WIDTH):
        base_x = 0
    pygame.display.update()

pygame.quit()
