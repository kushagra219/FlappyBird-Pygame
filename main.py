import random
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

clock = pygame.time.Clock()

bird_images = [pygame.image.load('assets/bird1.png'), 
pygame.image.load('assets/bird2.png'), pygame.image.load('assets/bird3.png')]
bird_image_static = pygame.image.load('assets/bird2.png')

pipe_up_image = pygame.image.load("assets/pipe.png")
pipe_down_image = pygame.transform.rotate(pipe_up_image, 180)

# Bird
class Bird:
    def __init__(self, x, y):
        self.image = bird_image_static
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 10
        self.score = 0
        self.animation_count = 0
        self.is_jump = False
        self.jump_count = 10

    def draw(self):
        self.jump()
        if self.is_jump == False:
            self.image = bird_image_static
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            self.image = bird_images[self.animation_count]
            self.rotate()
            screen.blit(self.image, (self.rect.x, self.rect.y))
            self.animation_count += 1
            if self.animation_count == 3:
                self.animation_count = 0

    def jump(self):
        if self.is_jump == False:
            self.rect.y += self.velocity * 0.8
            pass
        else:
            if self.jump_count > 0:
                self.rect.y -= (self.velocity + 2) ** 2 / 8 
            else:
                self.rect.y += self.velocity ** 2 / 8 
            
            self.jump_count -= 1
            if self.jump_count < -10:
                self.is_jump = False
                self.jump_count = 10

    def move(self):
        self.is_jump = True

    def rotate(self):
        if self.is_jump == True:
            if self.jump_count > 0:
                self.image = pygame.transform.rotate(self.image, 2 * self.jump_count)
            else:
                self.image = pygame.transform.rotate(self.image, 2 * self.jump_count)


# Pipe
class Pipe(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pipe_up_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 10

    def draw(self):
        self.move()
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(pipe_down_image, (self.rect.x, (SCREEN_HEIGHT - self.rect.y - 50) - 320))

    def move(self):
        self.rect.x -= 5

# Move base function 
def move_base():
    global base_x
    base_x -= 5
    if base_x <= -(SCREEN_WIDTH):
        base_x = 0
    screen.blit(base_img, (base_x, 400))
    screen.blit(base_img, (base_x + SCREEN_WIDTH, 400))


bird = Bird(100, 256)
list_of_pipes = []
PIPE_ADD_EVENT = pygame.USEREVENT
pygame.time.set_timer(PIPE_ADD_EVENT, 1500)

base_x = 0
run = True
while run:
    clock.tick(30) # FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.move()

        if event.type == PIPE_ADD_EVENT:
            pipe = Pipe(SCREEN_WIDTH, random.randint(250, 350))
            list_of_pipes.append(pipe)

    screen.blit(background_img, (0, 0))
    move_base()
    bird.draw()
    for pipe in list_of_pipes:
        pipe.draw()
    pygame.display.update()

pygame.quit()
