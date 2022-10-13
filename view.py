import tkinter as tk
from model import Storehouse, Worker
from constants import *


class TextView:
    def __init__(self) -> None:
        pass

    def draw(self,
             storehouse: Storehouse,
             worker: Worker) -> None:
        num_rows, num_cols = storehouse.get_dimension()

        for i in range(num_rows):
            row = ''
            for j in range(num_cols):
                if (i, j) == worker.get_pos():
                    row += worker.get_text()
                elif (i, j) in storehouse.get_boxes():
                    row += BOX
                else:
                    row += storehouse.get_tile(i, j).get_text()
            print(row)
