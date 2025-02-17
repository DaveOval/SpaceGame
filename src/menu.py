import pygame
import sys
from settings import *

def draw_text(screen, text, size, x, y, color = WHITE, selected = False):
    """
    Function to draw text on the screen
    """
    font = pygame.font.Font(None, size)

    if selected:
        font = pygame.font.Font(None, size + 10)

    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))

    if selected:
        pygame.draw.rect(screen, (255, 255, 255, 50), text_rect.inflate(20, 10), border_radius=10)

    screen.blit(text_surface, text_rect)

def menu():
    """
    Main menu of the game
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption( GAME_NAME )

    # Load the music and effects of the menu
    pygame.mixer.music.load(MENU_MUSIC)
    pygame.mixer.music.play(-1)
    click_sound = pygame.mixer.Sound(CLICK_SOUND)
    change_song = pygame.mixer.Sound(CHANGE_SOUND)

    # Load the backgorund image
    background = pygame.image.load( MENU_IMAGE )
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    selected = 0

    options = ["Play", "Credits" ,"Quit"]

    renning = True

    while renning:
        screen.blit(background, (0, 0))

        # Display the options
        for i, option in enumerate(options):
            is_selected = i == selected
            color = (0, 0,0 ) if i == selected else (200, 200, 200)
            draw_text(screen, option, 40, WIDTH // 2, 250 + i * 60, color, is_selected)

            if is_selected:
                pygame.draw.polygon(screen, WHITE, [(WIDTH // 2 - 100, 240 + i * 60), (WIDTH // 2 - 80, 250 + i * 60), (WIDTH // 2 - 100, 260 + i * 60)])

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    change_song.play()
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_UP:
                    change_song.play()
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    click_sound.play()
                    if options[selected] == "Play":
                        return "play"
                    elif options[selected] == "Credits":
                        return "credits"
                    elif options[selected] == "Quit":
                        pygame.quit()
                        sys.exit()
        clock.tick(FPS)