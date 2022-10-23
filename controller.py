from model import Model
from view import TextView, GraphicalView
from constants import *
import tkinter as tk
from tkinter import messagebox


class Controller:
    def __init__(self,
                 model: Model,
                 view: TextView) -> None:
        self._model = model
        self._view = view

    def draw(self) -> None:
        self._view.draw(self._model.get_room(), self._model.get_cat())
        print()

    def prompt_user(self) -> str:
        while True:
            command = input(PROMPT_TEXT).lower()
            if command in MOVE_CODES or command == END_GAME:
                return command

    def play(self) -> None:
        while True:
            self.draw()
            if self._model.room_messed():
                if self._model.all_room_messed():
                    print(WIN)
                    return
                else:
                    self._model.level_up()
                    _ = input(PRESS_ANY)
                    continue

            command = self.prompt_user()
            if command in MOVE_CODES:
                self._model.move_cat(MOVE_CODES[command])
            elif command == END_GAME:
                return


class GraphicalController:
    def __init__(self,
                 model: Model,
                 view: GraphicalView,
                 root: tk.Tk) -> None:
        self._model = model
        self._view = view
        self._root = root

    def _handle_keyboard(self, e: tk.Event) -> None:

        # just finished a room, skip one keyboard event and redraw the new room
        if self._model.skip_keyboard():
            self._model.keyboard_switch()
            self._view.update_canvas_imgs()
            self._redraw()
            return
        # general move and redraw the room
        if e.keycode in MOVE_CODES:
            self._model.move_cat(MOVE_CODES[e.keycode])
        else:
            return
        self._redraw()

        # check if the room is finished and attempt to get into next room
        if self._model.room_messed():
            if self._model.get_cur_room_num()+1 < self._model.get_num_rooms():
                self._model.level_up()
                self._view.set_room_dimension(self._model.get_room().get_dimension())
                return
            else:
                messagebox.showinfo(title=WIN_TITLE, message=WIN)
                self._root.destroy()
                return

    def _redraw(self) -> None:
        self._view.draw(self._model.get_cat(), self._model.get_room())

    def play(self) -> None:
        self._view.create_components(self._model.get_cur_dimension())
        self._view.bind_keyboard_callback(self._handle_keyboard)
        self._redraw()
