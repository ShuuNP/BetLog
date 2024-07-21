import pygame
import random
import joblib
import numpy as np
import os

# Ensure the transform script is executed before loading the model
if not os.path.exists('player_behavior_model.pkl'):
    import transform
    transform.transform_and_train("data_log.json", "player_behavior_model.pkl")

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Prototype Game")
clock = pygame.time.Clock()

# Load the trained model
model = joblib.load('player_behavior_model.pkl')

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Boundary checks
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, -5)
        player_bullet_group.add(bullet)

# AI Player class
class AIPlayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5

    def update(self):
        # Predict next action using the trained model
        features = np.array([self.rect.x, self.rect.y, pygame.time.get_ticks()]).reshape(1, -1)
        predicted_action = model.predict(features)[0]

        if predicted_action == 'move_left':
            self.rect.x -= self.speed
        elif predicted_action == 'move_right':
            self.rect.x += self.speed
        elif predicted_action == 'move_up':
            self.rect.y -= self.speed
        elif predicted_action == 'move_down':
            self.rect.y += self.speed
        elif predicted_action == 'shoot':
            self.shoot()

        # Boundary checks
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, -5)
        enemy_bullet_group.add(bullet)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

# Initialize player and bullet groups
player = Player()
ai_player = AIPlayer()
player_group = pygame.sprite.Group(player)
enemy_bullet_group = pygame.sprite.Group()
player_bullet_group = pygame.sprite.Group()
ai_player_group = pygame.sprite.Group(ai_player)

# Game phases
phase = 1
phase_timer = pygame.time.get_ticks()

# Main game loop
running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and phase == 2:
                player.shoot()

    # Phase transition logic
    if phase == 1 and pygame.time.get_ticks() - phase_timer > 10000:
        phase = 2
        phase_timer = pygame.time.get_ticks()
    elif phase == 2 and pygame.time.get_ticks() - phase_timer > 10000:
        phase = 1
        phase_timer = pygame.time.get_ticks()

    # Spawn bullets at intervals
    if phase == 1 and random.random() < 0.02:
        bullet = Bullet(random.randint(0, WIDTH), 0, 5)
        enemy_bullet_group.add(bullet)

    # Update sprites
    player_group.update()
    ai_player_group.update()
    enemy_bullet_group.update()
    player_bullet_group.update()

    # Check for collisions
    if phase == 1 and pygame.sprite.spritecollideany(player, enemy_bullet_group):
        print("Player hit!")
        running = False
    elif phase == 2 and pygame.sprite.groupcollide(player_bullet_group, enemy_bullet_group, True, True):
        print("Bullet hit!")

    # Draw everything
    screen.fill(WHITE)
    player_group.draw(screen)
    ai_player_group.draw(screen)
    enemy_bullet_group.draw(screen)
    player_bullet_group.draw(screen)

    # Render phase timer
    elapsed_time = (pygame.time.get_ticks() - phase_timer) / 1000
    timer_text = pygame.font.SysFont(None, 55).render(f'Time: {elapsed_time:.2f}', True, BLACK)
    screen.blit(timer_text, (10, 10))

    pygame.display.flip()

pygame.quit()
