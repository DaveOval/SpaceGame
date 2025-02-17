import pygame
from settings import *

class Enemy( pygame.sprite.Sprite ):
    def __init__(self, image_path, x, y, speed, health, damage):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (50, 50)) 
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.health = health
        self.damage = damage

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

LIGHT_ENEMY_IMAGE = "assets/images/enemies/light.png"
MEDIUM_ENEMY_IMAGE = "assets/images/enemies/medium.png"
HEAVY_ENEMY_IMAGE = "assets/images/enemies/heavy.png"

class LightEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(LIGHT_ENEMY_IMAGE, x, y, 2, 1, 1)

class MediumEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(MEDIUM_ENEMY_IMAGE, x, y, 1, 3, 2)

class HeavyEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(HEAVY_ENEMY_IMAGE, x, y, 1, 5, 3)