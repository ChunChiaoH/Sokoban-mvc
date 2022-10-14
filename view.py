import tkinter as tk
from model import *
from constants import *
from typing import Union, Callable
from PIL import ImageTk, Image

class TextView:
    def __init__(self) -> None:
        pass

    def draw(self,
             room: Room,
             cat: Cat) -> None:
        num_rows, num_cols = room.get_dimension()
        glasses = room.get_glasses()
        for i in range(num_rows):
            row = ''
            for j in range(num_cols):
                if (i, j) == cat.get_pos():
                    row += cat.get_text()
                elif (i, j) in glasses:
                    row += glasses[(i, j)].get_text()
                else:
                    row += room.get_tile(i, j).get_text()
            print(row)




