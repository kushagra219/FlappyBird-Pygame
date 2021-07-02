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

PIPE_GAP = 150
PIPE_HEIGHT = 320

# play music

# Bird
class Bird:
    def __init__(self, x, y):
        self.image = bird_image_static
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 0
        self.score = 0
        self.animation_count = 0
        self.is_jump = False
        self.jump_count = 0
        self.lives = 5

    def draw(self):
        self.jump()
        if self.is_jump == False:
            self.image = bird_image_static
        else:
            self.image = bird_images[self.animation_count]
            self.animation_count += 1
            if self.animation_count == 3:
                self.animation_count = 0
        # fourth change
        self.rotate()
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def jump(self):
        global is_game_started, is_game_over

        if self.is_jump == False:
            self.rect.y += self.velocity
        else:
            if self.jump_count > 0:
                self.rect.y -= (self.velocity + 2) ** 2 / 8
            else:
                self.rect.y += self.velocity ** 2 / 8

            # first change
            if self.jump_count < 0:
                self.is_jump = False

        # second change
        if self.jump_count > -10 and is_game_started and not is_game_over:
            self.jump_count -= 1

    def move(self):
        self.is_jump = True
        self.jump_count = 10

    def rotate(self):
        self.image = pygame.transform.rotate(self.image, 2 * self.jump_count)


# Pipe
class Pipe(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 10

    def draw(self):
        self.move()
        screen.blit(self.image, (self.rect.x, self.rect.y))
        # screen.blit(pipe_down_image, (self.rect.x, self.rect.y - PIPE_GAP - PIPE_HEIGHT))

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

# draw text function
def draw_text(string, font_size, font_color, x, y):
    font = pygame.font.SysFont('Comic Sans', font_size)
    text = font.render(string, True, font_color)
    text_rect = text.get_rect()
    text_rect.centerx = x
    text_rect.y = y
    screen.blit(text, text_rect)


bird = Bird(100, 256)
list_of_pipes = []
PIPE_ADD_EVENT = pygame.USEREVENT
pygame.time.set_timer(PIPE_ADD_EVENT, 1600)

is_game_started = False
is_game_over = False
base_x = 0
run = True
while run:
    clock.tick(30)  # FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # start game
                if is_game_started == False:
                    is_game_started = True
                    bird.velocity = 5
                # restart game
                elif is_game_over == True:
                    is_game_over = False
                    bird.velocity = 5
                    bird.lives = 5
                    bird.score = 0
                # during gameplay
                else:
                    # wing_sound.play()
                    bird.move()

        if event.type == PIPE_ADD_EVENT and is_game_started and not is_game_over:
            lower_pipe = Pipe(SCREEN_WIDTH, random.randint(200, 375), pipe_up_image)
            upper_pipe = Pipe(SCREEN_WIDTH, lower_pipe.rect.y - PIPE_GAP - PIPE_HEIGHT, pipe_down_image)
            bird.score += 1
            list_of_pipes.append(lower_pipe)
            list_of_pipes.append(upper_pipe)

    screen.blit(background_img, (0, 0))

    if is_game_started == False:
        draw_text("Press SPACE to start", 30, RED, SCREEN_WIDTH//2, 150)

    if is_game_over == True:
        draw_text("Game over!", 30, RED, SCREEN_WIDTH//2, 150)
        draw_text("Press SPACE to restart", 30, RED, SCREEN_WIDTH//2, 200)

    move_base()
    bird.draw()
    for pipe in list_of_pipes:
        pipe.draw()
        if bird.rect.colliderect(pipe):
            bird.rect.x = 100
            bird.rect.y = 256
            bird.lives -= 1
            draw_text("-1", 30, RED, bird.rect.x, bird.rect.y)
            list_of_pipes.clear()
            # hit_sound.play()
            if bird.lives == 0:
                is_game_over = True
                bird.jump_count = 0
                bird.velocity = 0
            pygame.display.update()
            pygame.time.delay(500)

    # boundary conditions
    if bird.rect.y + bird.rect.height >= 400:
        bird.rect.x = 100
        bird.rect.y = 256
        bird.lives -= 1
        draw_text("-1", 30, RED, bird.rect.x, bird.rect.y)
        list_of_pipes.clear()
        # hit_sound.play()
        if bird.lives == 0:
            is_game_over = True
            bird.jump_count = 0
            bird.velocity = 0
        pygame.display.update()
        pygame.time.delay(500)

    for pipe in list_of_pipes:
        # remove pipe when it is out of the screen 
        if pipe.rect.x < -100:
            list_of_pipes.remove(pipe)


    draw_text(f"Lives: {bird.lives}", 30, WHITE, 40, 10)
    draw_text(f"Score: {bird.score}", 30, WHITE, SCREEN_WIDTH-45, 10)

    pygame.display.update()

pygame.quit()

# Homework 
# 1 - (Make a game using pygame)
# 2 - (Hacerrank 5* Python)


