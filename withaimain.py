import pygame
import random
import sys
import time
from datacollection import *
from decisiontree import model

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
BULLET_SIZE = 20
BULLET_SPEED = 5
PLAYER_SPEED = 5
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Bullets!")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
player = pygame.Rect(WIDTH // 2, HEIGHT - PLAYER_SIZE - 10, PLAYER_SIZE, PLAYER_SIZE)

bullets = []

def create_bullet():
    x = random.randint(0, WIDTH - BULLET_SIZE)
    bullet = pygame.Rect(x, 0, BULLET_SIZE, BULLET_SIZE)
    bullets.append(bullet)

def move_bullets():
    for bullet in bullets:
        bullet.y += BULLET_SPEED
    bullets[:] = [bullet for bullet in bullets if bullet.y < HEIGHT]

def check_collision():
    for bullet in bullets:
        if player.colliderect(bullet):
            return True
    return False

def draw_text(text, x, y):
    screen.blit(font.render(text, True, WHITE), (x, y))
    
def ai_play(player_position, current_time):
    action = model.predict([[player_position, current_time]])
    return 'move_left' if action == 0 else 'move_right'

def game_loop():
    score = 0
    game_over = False
    pygame.time.set_timer(pygame.USEREVENT, 1000) 

    start_time = time.time()  

    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_data_log()  
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT and not game_over:
                create_bullet()

        keys = pygame.key.get_pressed()
        
        
        current_time = time.time() - start_time  

        if not game_over:
            ai_action = ai_play(player.x, current_time)
            if ai_action == 'move_left' and player.x - PLAYER_SPEED > 0:
                player.x -= PLAYER_SPEED
            if ai_action == 'move_right' and player.x + PLAYER_SPEED < WIDTH - PLAYER_SIZE:
                player.x += PLAYER_SPEED

        move_bullets()

        if not game_over:
            game_over = check_collision()
            if not game_over:
                score += 1 / FPS

        pygame.draw.rect(screen, BLUE, player)
        for bullet in bullets:
            pygame.draw.rect(screen, RED, bullet)

        draw_text(f"Score: {int(score)}", 10, 10)

        if game_over:
            draw_text("Game Over! Press R to Restart", WIDTH // 2 - 150, HEIGHT // 2)
            if keys[pygame.K_r]:
                save_data_log()  
                game_loop()

        pygame.display.flip()
        clock.tick(FPS)


game_loop()
