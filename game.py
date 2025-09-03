import pygame
import sys
import random
import os
import time

# Initialize pygame
pygame.init()

# Screen
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# Load images
bg = pygame.image.load("background.png").convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

bird_img = pygame.image.load("bird.png").convert_alpha()
bird_img = pygame.transform.scale(bird_img, (40, 30))

pipe_width, pipe_height = 70, 400
PIPE_GAP = 160
pipe_speed = 4

# Heart
heart_img = pygame.image.load("heart.png").convert_alpha()
heart_img = pygame.transform.scale(heart_img, (30, 30))

# Bird
bird_x, bird_y = 50, HEIGHT // 2
bird_y_change = 0
gravity = 0.6
jump = -10

# Pipes
pipes = []

# Score & lives
score = 0
lives = 3
game_over = False

# Heart timer
last_heart_loss_time = time.time()
HEART_LOSS_INTERVAL = 10  # seconds

# Highscore
if not os.path.exists("highscore.txt"):
    with open("highscore.txt", "w") as f:
        f.write("0")
with open("highscore.txt", "r") as f:
    highscore = int(f.read())

def reset_game():
    global bird_x, bird_y, bird_y_change, pipes, score, game_over, lives, last_heart_loss_time
    bird_x, bird_y = 50, HEIGHT // 2
    bird_y_change = 0
    pipes = []
    score = 0
    lives = 3
    game_over = False
    last_heart_loss_time = time.time()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and not game_over:
            bird_y_change = jump
        if event.type == pygame.KEYDOWN and game_over:
            reset_game()

    if not game_over:
        # Bird
        bird_y_change += gravity
        bird_y += bird_y_change

        # Pipes
        if len(pipes) == 0 or pipes[-1][0] < WIDTH - 200:
            pipe_height = random.randint(100, 300)
            pipes.append([WIDTH, pipe_height])

        for pipe in pipes:
            pipe[0] -= pipe_speed
            if pipe[0] + pipe_width < 0:
                pipes.remove(pipe)
                score += 1
                if score > highscore:
                    highscore = score

        # Collision
        for (pipe_x, pipe_y) in pipes:
            top_rect = pygame.Rect(pipe_x, 0, pipe_width, pipe_y)
            bottom_rect = pygame.Rect(pipe_x, pipe_y + PIPE_GAP, pipe_width, HEIGHT)
            bird_rect = bird_img.get_rect(topleft=(bird_x, bird_y))

            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                lives -= 1
                pipes.clear()  # reset pipes after hit
                bird_y = HEIGHT // 2
                if lives <= 0:
                    game_over = True

        if bird_y <= 0 or bird_y >= HEIGHT - 30:
            lives -= 1
            bird_y = HEIGHT // 2
            if lives <= 0:
                game_over = True

        # Timer-based life loss
        if time.time() - last_heart_loss_time > HEART_LOSS_INTERVAL:
            lives -= 1
            last_heart_loss_time = time.time()
            if lives <= 0:
                game_over = True

    # Draw background
    screen.blit(bg, (0, 0))

    # Pipes
    for (pipe_x, pipe_y) in pipes:
        pygame.draw.rect(screen, (0, 200, 0), (pipe_x, 0, pipe_width, pipe_y))
        pygame.draw.rect(screen, (0, 200, 0), (pipe_x, pipe_y + PIPE_GAP, pipe_width, HEIGHT))

    # Bird
    screen.blit(bird_img, (bird_x, bird_y))

    # Score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    highscore_text = font.render(f"Highscore: {highscore}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(highscore_text, (10, 40))

    # Lives (hearts)
    for i in range(lives):
        screen.blit(heart_img, (WIDTH - 40 - i * 35, 10))

    if game_over:
        over_text = font.render("Game Over! Press any key", True, (255, 0, 0))
        screen.blit(over_text, (40, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(30)