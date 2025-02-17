import pygame
from settings import *
import random
from classes.enemyClass import LightEnemy, MediumEnemy, HeavyEnemy
from classes.obstacleClass import MeteorObstacle, MineObstacle

class Game:
    def __init__(self, selected_ship_class):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_NAME)

        # Initialize player ship
        self.selected_ship = selected_ship_class

        # Groups to manage all game sprites
        self.all_sprites = pygame.sprite.Group(self.selected_ship)
        self.bullets_group = pygame.sprite.Group()
        self.enemies_group = pygame.sprite.Group()
        self.obstacles_group = pygame.sprite.Group()

        self.clock = pygame.time.Clock()
        self.running = True
        self.level = 1

        # Enemy spawn settings
        self.enemy_spawn_rate = 1000  # Spawn enemy every 1000ms
        self.last_enemy_spawn = pygame.time.get_ticks()

        # Obstacle spawn settings
        self.obstacle_spawn_rate = 5000  # Spawn obstacle every 5000ms
        self.last_obstacle_spawn = pygame.time.get_ticks()

    def check_collisions(self):
        """
        Check for collisions between bullets and enemies, and between the player ship and obstacles.
        """
        # Collision between bullets and enemies
        for bullet in self.bullets_group:
            enemies_hit = pygame.sprite.spritecollide(bullet, self.enemies_group, False)
            for enemy in enemies_hit:
                enemy.take_damage(10)
                bullet.kill()

        # Collision between player and obstacles
        if pygame.sprite.spritecollide(self.selected_ship, self.obstacles_group, False):
            self.selected_ship.health -= 10
            if self.selected_ship.health <= 0:
                self.game_over()

    def spawn_enemies(self):
        """
        Spawn enemies at random positions at the top of the screen at set intervals.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_spawn > self.enemy_spawn_rate:
            enemy_type = random.choice([LightEnemy, MediumEnemy, HeavyEnemy])
            x = random.randint(50, WIDTH - 50)  # Ensure enemy spawns within screen bounds
            y = -50  # Start off-screen
            enemy = enemy_type(x, y)
            self.enemies_group.add(enemy)
            self.all_sprites.add(enemy)
            self.last_enemy_spawn = current_time

    def spawn_obstacle(self):
        """
        Spawn obstacles at random positions at the top of the screen at set intervals.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_obstacle_spawn > self.obstacle_spawn_rate:
            obstacle_type = random.choice([MeteorObstacle, MineObstacle])
            x = random.randint(50, WIDTH - 50)  # Ensure obstacle spawns within screen bounds
            y = -50  # Start off-screen
            obstacle = obstacle_type(x, y)
            self.obstacles_group.add(obstacle)
            self.all_sprites.add(obstacle)
            self.last_obstacle_spawn = current_time

    def game_over(self):
        """
        Display game over message and stop the game loop.
        """
        print("Game Over")
        self.running = False

    def update(self):
        """
        Update all game elements.
        """
        self.all_sprites.update()  # Update all sprites (player, bullets, enemies, obstacles)
        self.check_collisions()
        self.spawn_enemies()
        self.spawn_obstacle()

    def draw(self):
        """
        Draw all game elements on the screen.
        """
        self.screen.fill(BLACK)  # Set background color to black
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def handle_events(self):
        """
        Handle player input and game events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def run(self):
        """
        Main game loop.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
