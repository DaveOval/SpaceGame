import pygame
from settings import *
from classes.bulletClass import Bullet

class Ship(pygame.sprite.Sprite):
    def __init__(self, x , y, speed, fire_rate, health, image_path, bullet_image, special_bullet_image, bullets_group, all_sprites):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (50, 50)) 
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.fire_rate = fire_rate 
        self.health = health
        self.last_shot = pygame.time.get_ticks() 
        self.bullet_image = bullet_image
        self.special_bullet_image = special_bullet_image
        self.bullets_group = bullets_group
        self.all_sprites = all_sprites
        self.normal_sound = pygame.mixer.Sound("assets/sounds/normal_shoot.wav")

    def move(self):
        """
        Movement of the ship wit AWSD 
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def shoot(self):
        """
        Method to shoot bullets from the ship
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.fire_rate:
            bullet = Bullet(self.rect.centerx, self.rect.top, self.bullet_image, -8)
            self.normal_sound.play()
            self.bullets_group.add(bullet)
            self.all_sprites.add(bullet)
            self.last_shot = current_time

    def special_shoot(self):
        """
        Method to shoot special bullets from the ship
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.fire_rate * 2:  
            bullet_left = Bullet(self.rect.left + 10, self.rect.top, self.special_bullet_image, -8)
            bullet_right = Bullet(self.rect.right - 10, self.rect.top, self.special_bullet_image, -8)
            self.bullets_group.add(bullet_left)
            self.bullets_group.add(bullet_right)
            self.all_sprites.add(bullet_left)
            self.all_sprites.add(bullet_right)
            self.last_shot = current_time

    def update(self):
        self.move()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:  
            self.shoot()
        if keys[pygame.K_LCTRL]:  
            self.special_shoot()

# Ligh ship class
LIGHT_SHIP_IMAGE = "assets/images/player/light.png"
LIGHT_BULLET = "assets/images/player/light_bullet.png"
LIGHT_SPECIAL_BULLET = "assets/images/player/light_special_bullet.png"

class LightShip(Ship):
    def __init__(self, x, y, bullets_group, all_sprites):
        super().__init__(x, y, 6, 200, 50, LIGHT_SHIP_IMAGE, LIGHT_BULLET, LIGHT_SPECIAL_BULLET, bullets_group, all_sprites)
        self.sound = pygame.mixer.Sound("assets/sounds/triple_shoot.wav")
    
    def special_shoot(self):
        """
        Fast shot with 3 bullets in fan shape
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.fire_rate * 2:
            self.sound.play()
            bullet_center = Bullet(self.rect.centerx, self.rect.top, self.special_bullet_image, -10)
            bullet_left = Bullet(self.rect.left + 5, self.rect.top, self.special_bullet_image, -8, -3)
            bullet_right = Bullet(self.rect.right - 5, self.rect.top, self.special_bullet_image, -8, 3)
            
            self.bullets_group.add(bullet_center)
            self.bullets_group.add(bullet_left)
            self.bullets_group.add(bullet_right)
            
            self.all_sprites.add(bullet_center)
            self.all_sprites.add(bullet_left)
            self.all_sprites.add(bullet_right)
            
            self.last_shot = current_time

# Medium ship class
MEDIUM_SHIP_IMAGE = "assets/images/player/medium.png"
MEDIUM_BULLET = "assets/images/player/medium_bullet.png"
MEDIUM_SPECIAL_BULLET = "assets/images/player/medium_special_bullet.png"
 
class MediumShip(Ship):
    def __init__(self, x, y, bullets_group, all_sprites):
        super().__init__(x, y, 4, 400, 100, MEDIUM_SHIP_IMAGE, MEDIUM_BULLET, MEDIUM_SPECIAL_BULLET, bullets_group, all_sprites)
        self.sound = pygame.mixer.Sound("assets/sounds/double_shoot.wav")

    def special_shoot(self):
        """
        Shoots double bullets straight
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.fire_rate * 2:
            self.sound.play()
            self.bullets_group.add(
                Bullet(self.rect.left + 10, self.rect.top, self.special_bullet_image, -8),
                Bullet(self.rect.right - 10, self.rect.top, self.special_bullet_image, -8)
            )
            self.last_shot = current_time

# Heavy ship class
HEAVY_SHIP_IMAGE = "assets/images/player/heavy.png"
HEAVY_BULLET = "assets/images/player/heavy_bullet.png"
HEAVY_SPECIAL_BULLET = "assets/images/player/heavy_special_bullet.png"

class HeavyShip(Ship):
    def __init__(self, x, y, bullets_group, all_sprites):
        super().__init__(x, y, 2, 600, 200, HEAVY_SHIP_IMAGE, HEAVY_BULLET, HEAVY_SPECIAL_BULLET, bullets_group, all_sprites)
        self.sound = pygame.mixer.Sound("assets/sounds/laser.wav")

    def special_shoot(self):
        """
        Shootsa strong ligh laser
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.fire_rate * 3:
            self.sound.play()
            self.bullets_group.add(
                Bullet(self.rect.centerx, self.rect.top, self.special_bullet_image, -15)
            )
            self.last_shot = current_time