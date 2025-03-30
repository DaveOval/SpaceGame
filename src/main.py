from screens import loading_screen, credits_screen
from menu import menu
from ship_selector import select_ship
from classes.gameClass import Game

if __name__ == "__main__":
    # Call the loading screen
    loading_screen()
    
    action = menu()

    if action == "credits": 
        credits_screen()
    
    if action == "play":
        # First we need to select the ship
        selected_ship = select_ship()
        print(selected_ship)
        game = Game(selected_ship)
        game.run()

    