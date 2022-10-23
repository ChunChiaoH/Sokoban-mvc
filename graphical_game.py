import model
import view
import controller
from constants import *
import tkinter as tk

def main() -> None:
    root = tk.Tk()
    game_model = model.Model(DEFAULT_GAMES)
    runner = controller.GraphicalController(game_model, view.GraphicalView(root), root)
    runner.play()
    root.mainloop()
    return

if __name__ == "__main__":
    main()