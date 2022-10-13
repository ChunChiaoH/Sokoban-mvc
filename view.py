import tkinter as tk
from model import Room, Cat
from constants import *


class TextView:
    def __init__(self) -> None:
        pass

    def draw(self,
             playground: Room,
             cat: Cat) -> None:
        num_rows, num_cols = playground.get_dimension()

        for i in range(num_rows):
            row = ''
            for j in range(num_cols):
                if (i, j) == cat.get_pos():
                    row += cat.get_text()
                elif (i, j) in playground.get_glasses():
                    row += GLASS
                else:
                    row += playground.get_tile(i, j).get_text()
            print(row)
