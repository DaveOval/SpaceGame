import pygame 

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, speed ,horisontal_speed = 0):
        print(f"Bullet created at {x}, {y}") 
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.horisontal_speed = horisontal_speed

    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.horisontal_speed
        print(f"Bullet position: {self.rect.x}, {self.rect.y}")
        if self.rect.bottom < 0:
            self.kill()