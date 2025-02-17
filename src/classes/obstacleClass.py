import pygame
from settings import *

class Obstacle( pygame.sprite.Sprite ):
    def __init__(self, x, y, image_path, damage, size):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(center=(x, y))
        self.damage = damage


    def update(self):
        self.rect.y += 2
        if self.rect.top > HEIGHT:
            self.kill()

METEOR_IMAGE = "assets/images/obstacles/meteor.png"
def MeteorObstacle(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/images/obstacles/meteor.png", 1, (50, 50))

MINE_IMAGE = "assets/images/obstacles/mine.png"
def MineObstacle(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/images/obstacles/mine.png", 2, (50, 50))
