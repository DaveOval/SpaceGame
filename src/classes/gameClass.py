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

        # Groups to manage all game sprites
        self.all_sprites = pygame.sprite.Group()
        self.bullets_group = pygame.sprite.Group()
        self.enemies_group = pygame.sprite.Group()
        self.obstacles_group = pygame.sprite.Group()

        # Initialize player ship
        self.selected_ship = selected_ship_class(WIDTH // 2, HEIGHT - 100, self.bullets_group, self.all_sprites)
        self.all_sprites.add(self.selected_ship)

        self.clock = pygame.time.Clock()
        self.running = True
        self.level = 1
        self.score = 0
        self.enemies_killed = 0
        self.level_threshold = 10  # Enemigos que hay que derrotar para subir de nivel

        # Enemy spawn settings
        self.enemy_spawn_rate = 1000  # Spawn enemy every 1000ms
        self.last_enemy_spawn = pygame.time.get_ticks()

        # Obstacle spawn settings
        self.obstacle_spawn_rate = 5000  # Spawn obstacle every 5000ms
        self.last_obstacle_spawn = pygame.time.get_ticks()

        # Font for score and level display
        self.font = pygame.font.Font(None, 36)

    def check_collisions(self):
        """
        Check for collisions between bullets and enemies, and between the player ship and obstacles.
        """
        # Collision between bullets and enemies
        for bullet in self.bullets_group:
            enemies_hit = pygame.sprite.spritecollide(bullet, self.enemies_group, False)
            for enemy in enemies_hit:
                enemy.take_damage(10)
                if enemy.health <= 0:
                    self.enemies_killed += 1
                    self.score += 10
                    # Check if we should level up
                    if self.enemies_killed >= self.level_threshold:
                        self.level_up()
                bullet.kill()

        # Collision between player and obstacles
        if pygame.sprite.spritecollide(self.selected_ship, self.obstacles_group, False):
            self.selected_ship.health -= 10
            if self.selected_ship.health <= 0:
                self.game_over()

        # Collision between enemies and player
        if pygame.sprite.spritecollide(self.selected_ship, self.enemies_group, False):
            self.selected_ship.health -= 10
            if self.selected_ship.health <= 0:
                self.game_over()

    def level_up(self):
        """
        Increase the level and adjust game difficulty
        """
        self.level += 1
        self.enemies_killed = 0
        self.level_threshold += 5  # Aumentar el umbral para el siguiente nivel
        
        # Aumentar la dificultad
        self.enemy_spawn_rate = max(300, self.enemy_spawn_rate - 100)  # Más rápido spawn de enemigos
        self.obstacle_spawn_rate = max(2000, self.obstacle_spawn_rate - 500)  # Más obstáculos
        
        # Limpiar la pantalla de enemigos y obstáculos
        for enemy in self.enemies_group:
            enemy.kill()
        for obstacle in self.obstacles_group:
            obstacle.kill()
            
        # Mostrar mensaje de nivel
        self.show_level_up_message()

    def show_level_up_message(self):
        """
        Display a level up message
        """
        message = f"Level {self.level}!"
        text = self.font.render(message, True, (255, 255, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)  # Mostrar el mensaje por 2 segundos

    def spawn_enemies(self, level=1, difficulty="normal"):
        """
        Spawn enemies at random positions at the top of the screen at set intervals.
        Probabilidad de aparición basada en el nivel y dificultad.

        Dificultades:
        - "easy": Más LightEnemy, menos HeavyEnemy
        - "normal": Distribución balanceada
        - "hard": Más MediumEnemy y HeavyEnemy

        Probability of enemy types:
        - LightEnemy: Variable
        - MediumEnemy: Variable
        - HeavyEnemy: Variable
        """
        # Base probability of enemy types
        enemy_probabilities = {
            1: [50, 30, 20],  # Level 1
            2: [40, 30, 30],  # Level 2
            3: [30, 30, 40],  # Level 3
            4: [20, 30, 50],  # Level 4
            5: [10, 30, 60]   # Level 5 o more
        }
        # Adjust based on difficulty
        difficulty_modifier = {
            "easy": [10, -10, -10],  # Más Light, menos Heavy y Medium
            "normal": [0, 0, 0],  # Sin cambios
            "hard": [-10, +10, +10]  # Más Medium y Heavy, menos Light
        }

        # Calculate adjusted probabilities
        lightProb, mediumProb, heavyProb = enemy_probabilities.get(level, [10, 30, 60])

        # Adjust probabilities based on difficulty
        diff_modifier = difficulty_modifier.get(difficulty, [0, 0, 0])
        lightProb = max(0, lightProb + diff_modifier[0])
        mediumProb = max(0, mediumProb + diff_modifier[1])
        heavyProb = max(0, heavyProb + diff_modifier[2])

        # Normalize probabilities
        total = lightProb + mediumProb + heavyProb
        if total > 0:
            lightProb = int((lightProb / total) * 100)
            mediumProb = int((mediumProb / total) * 100)
            heavyProb = int((heavyProb / total) * 100)

        # Spawn enemies
        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_spawn > self.enemy_spawn_rate:
            enemy_type = random.choices(
                [LightEnemy, MediumEnemy, HeavyEnemy],
                weights=[lightProb, mediumProb, heavyProb],
                k=1
            )[0]

            x = random.randint(50, WIDTH - 50)  # Spawn dentro de los límites de la pantalla
            y = -50  # Iniciar fuera de la pantalla
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
        
        # Draw HUD
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        progress_text = self.font.render(f"Progress: {self.enemies_killed}/{self.level_threshold}", True, WHITE)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 40))
        self.screen.blit(progress_text, (10, 70))
        
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
