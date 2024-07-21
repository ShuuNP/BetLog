import pygame
import random
import time
from datacollection import log_data, save_data_log

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Prototype Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 55)

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
            log_data("move_left", (self.rect.x, self.rect.y), pygame.time.get_ticks())
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            log_data("move_right", (self.rect.x, self.rect.y), pygame.time.get_ticks())
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            log_data("move_up", (self.rect.x, self.rect.y), pygame.time.get_ticks())
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            log_data("move_down", (self.rect.x, self.rect.y), pygame.time.get_ticks())

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
        log_data("shoot", (self.rect.centerx, self.rect.top), pygame.time.get_ticks())

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

player = Player()
player_group = pygame.sprite.Group(player)
enemy_bullet_group = pygame.sprite.Group()
player_bullet_group = pygame.sprite.Group()

phase = 1
phase_timer = pygame.time.get_ticks()

running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and phase == 2:
                player.shoot()

    if phase == 1 and pygame.time.get_ticks() - phase_timer > 10000:
        phase = 2
        phase_timer = pygame.time.get_ticks()
    elif phase == 2 and pygame.time.get_ticks() - phase_timer > 10000:
        phase = 1
        phase_timer = pygame.time.get_ticks()

    if phase == 1 and random.random() < 0.02:
        bullet = Bullet(random.randint(0, WIDTH), 0, 5)
        enemy_bullet_group.add(bullet)

    player_group.update()
    enemy_bullet_group.update()
    player_bullet_group.update()

    # Check for collisions
    if phase == 1 and pygame.sprite.spritecollideany(player, enemy_bullet_group):
        print("Player hit!")
        running = False
    elif phase == 2 and pygame.sprite.groupcollide(player_bullet_group, enemy_bullet_group, True, True):
        print("Bullet hit!")

    screen.fill(WHITE)
    player_group.draw(screen)
    enemy_bullet_group.draw(screen)
    player_bullet_group.draw(screen)

    elapsed_time = (pygame.time.get_ticks() - phase_timer) / 1000
    timer_text = font.render(f'Time: {elapsed_time:.2f}', True, BLACK)
    screen.blit(timer_text, (10, 10))

    pygame.display.flip()

pygame.quit()

save_data_log("data_log.json")
