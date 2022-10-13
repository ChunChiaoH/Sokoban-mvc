import model
import view
import controller
from constants import *
import os

def main() -> None:
    """Entry-point to start the game"""
    # prompt for gamefile directory and start the game
    game_file = input(GAMEFILE_TEXT)
    if not os.path.exists(game_file):
        print(DIR_NOT_EXIST)
        game_file = DEFAULT_GAMES
    game_model = model.Model(game_file)
    runner = controller.Controller(game_model, view.TextView())
    runner.play()
    return

if __name__ == "__main__":
    main()