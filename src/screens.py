import pygame
import time
from settings import *

def loading_screen():
    """
    Function to display the loading screen
    """
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption( GAME_NAME )
    
    # Load the backgorund image
    background = pygame.image.load( LOADING_IMAGE )
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))


    screen.blit(background, (0, 0))
    pygame.display.flip()

    time.sleep(3)  

def credits_screen():
    """
    Function to display the credits screen
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption( GAME_NAME )
    
    # Load the backgorund image
    background = pygame.image.load( CREDITS_IMAGE )
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    font = pygame.font.Font(None, 40)

    credits = [
        GAME_NAME,
        "Developed by: David Vazquez",
        "Music by: opengameart.org",
        "Thanks for playing!"
    ]

    y_offset = HEIGHT

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.blit(background, (0, 0))

        # Display the credits
        for i, line in enumerate(credits):
            text_surface = font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, y_offset + i * 50))
            screen.blit(text_surface, text_rect)

        y_offset -= 1
        pygame.display.flip()

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                running = False

def gameOverScreen():
    """
    Function to display the game over screen
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption( GAME_NAME )
    
    # Load the backgorund image
    background = pygame.image.load( GAME_OVER_IMAGE )
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    font = pygame.font.Font(None, 40)

    game_over = [
        "Game Over",
        "Press any key to continue"
    ]

    y_offset = HEIGHT

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.blit(background, (0, 0))

        # Display the game over message
        for i, line in enumerate(game_over):
            text_surface = font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, y_offset + i * 50))
            screen.blit(text_surface, text_rect)

        y_offset -= 1
        pygame.display.flip()

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                running = False