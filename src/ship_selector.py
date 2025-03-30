import pygame
from settings import * 
from classes.shipClass import LightShip, MediumShip, HeavyShip

def draw_text(screen, text, size, x, y, color=WHITE):
    """
    Helper function to draw text on the screen.
    """
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def select_ship():
    """
    Display the ship selection screen and return the chosen ship.
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Select Your Starfighter")

    LIGHT_SHIP_IMAGE = "assets/images/player/light.png"
    MEDIUM_SHIP_IMAGE = "assets/images/player/medium.png"
    HEAVY_SHIP_IMAGE = "assets/images/player/heavy.png"

    click_sound = pygame.mixer.Sound(CLICK_SOUND)
    change_song = pygame.mixer.Sound(CHANGE_SOUND)

    ships = [
        {
            "name": "Phantom Striker", 
            "class": LightShip, 
            "image": pygame.image.load(LIGHT_SHIP_IMAGE),
            "speed": "■■■■■",
            "fire_rate": "■■■■",
            "health": "■■",
        },
        {
            "name": "Titan Guardian", 
            "class": MediumShip, 
            "image": pygame.image.load(MEDIUM_SHIP_IMAGE),
            "speed": "■■■",
            "fire_rate": "■■■",
            "health": "■■■■"
        },
        {
            "name": "Doombringer", 
            "class": HeavyShip, 
            "image": pygame.image.load(HEAVY_SHIP_IMAGE),
            "speed": "■■",
            "fire_rate": "■■",
            "health": "■■■■■■"
        }
    ]

    selected = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill((0, 0, 30)) 
        
        # Definir el ancho de la pantalla dividido en dos partes
        ship_area_width = WIDTH // 2
        info_area_width = WIDTH - ship_area_width
        
        # Mostrar imágenes de las naves a la izquierda
        for i, ship in enumerate(ships):
            ship_img = pygame.transform.scale(ship["image"], (120, 120))

            x = ship_area_width // 2 - 75
            y = 100 + i * 160

            if i == selected:
                pygame.draw.rect(screen, (255, 255, 255), (x - 10, y - 10, 170, 170), 3)

            screen.blit(ship_img, (x, y))

        # Mostrar información de la nave seleccionada a la derecha
        selected_ship = ships[selected]
        
        # Fondo para la sección de la información
        pygame.draw.rect(screen, (20, 20, 60), (ship_area_width + 10, 50, info_area_width - 20, HEIGHT - 100), border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), (ship_area_width + 10, 50, info_area_width - 20, HEIGHT - 100), 2, border_radius=10)
        
        # Mostrar texto de la nave seleccionada
        draw_text(screen, selected_ship["name"], 40, WIDTH // 2 + ship_area_width // 2, 100, WHITE)
        draw_text(screen, f"Speed: {selected_ship['speed']}", 30, WIDTH // 2 + ship_area_width // 2, HEIGHT // 2 - 60, WHITE)
        draw_text(screen, f"Fire Rate: {selected_ship['fire_rate']}", 30, WIDTH // 2 + ship_area_width // 2, HEIGHT // 2, WHITE)
        draw_text(screen, f"Health: {selected_ship['health']}", 30, WIDTH // 2 + ship_area_width // 2, HEIGHT // 2 + 60, WHITE)
        draw_text(screen, "Press ENTER to select", 30, WIDTH // 2 + ship_area_width // 2, HEIGHT - 100, (200, 200, 200))

        pygame.display.flip()

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    change_song.play()
                    selected = (selected + 1) % len(ships)
                elif event.key == pygame.K_UP:
                    change_song.play()
                    selected = (selected - 1) % len(ships)
                elif event.key == pygame.K_RETURN:
                    click_sound.play()
                    return ships[selected]["class"]

        clock.tick(FPS)
