import os
from model import Model
from view import TextView
from constants import *


class Controller():
    def __init__(self,
                 model: Model,
                 view: TextView) -> None:
        self._model = model
        self._view = view

    def draw(self) -> None:
        self._view.draw(self._model.get_storehouse(), self._model.get_worker())
        print()

    def prompt_user(self) -> str:
        while True:
            command = input(PROMPT_TEXT).lower()
            if command in MOVES or command == END_GAME:
                return command

    def play(self) -> None:
        while True:
            self.draw()
            if self._model.storehouse_finished():
                if self._model._cur_lv + 1 < self._model.get_num_storehouses():
                    self._model.level_up()
                    _ = input(PRESS_ANY)
                    continue
                else:
                    print(WIN)
                    return

            command = self.prompt_user()
            if command in MOVES:
                self._model.move_worker(MOVES[command])
            elif command == END_GAME:
                return
