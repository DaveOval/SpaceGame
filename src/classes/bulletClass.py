import pygame 

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, speed ,horisontal_speed = 0):
        print(f"Bullet created at {x}, {y}") 
        super().__init__()
        # self.image = pygame.image.load(image_path)
        # self.image = pygame.transform.scale(self.image, (10, 30)) # Scale the image to 10x10 pixels for the game window
        self.image = pygame.Surface((10, 30))  
        self.image.fill((255, 0, 0))  
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.horisontal_speed = horisontal_speed

    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.horisontal_speed
        print(f"Bullet position: {self.rect.x}, {self.rect.y}")
        if self.rect.bottom < 0:
            self.kill()