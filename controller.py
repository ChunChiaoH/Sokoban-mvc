from model import Model
from view import TextView, GraphicalView
from constants import *
from ai_solver import SokobanSolver
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
            valid_chars = [info['char'] for info in MOVE_DIRECTIONS.values()]
            if command in valid_chars or command == END_GAME:
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
            move_delta = next((info['delta'] for info in MOVE_DIRECTIONS.values() 
                             if info['char'] == command), None)
            if move_delta:
                self._model.move_cat(move_delta)
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
        self._solver = SokobanSolver(model)
        self._solution = None
        self._solving = False

    def _handle_keyboard(self, e: tk.Event) -> None:

        # just finished a room, skip one keyboard event and redraw the new room
        if self._model.skip_keyboard():
            self._model.keyboard_switch()
            self._view.update_canvas_imgs()
            self._redraw()
            return
        
        # AI solver commands
        if e.keysym.lower() == 'x':  # Changed from 's' to 'x' to avoid conflict
            self._solve_with_ai()
            return
        elif e.keysym.lower() == 'h':
            self._get_hint()
            return
        
        # general move and redraw the room
        move_delta = None
        for info in MOVE_DIRECTIONS.values():
            if e.keycode in info['keys']:
                move_delta = info['delta']
                break
        
        if move_delta:
            self._model.move_cat(move_delta)
            self._redraw()
        else:
            return

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
    
    def _solve_with_ai(self) -> None:
        """Solve the current puzzle using AI and show solution step by step."""
        if self._solving:
            return
        
        self._solving = True
        messagebox.showinfo(AI_SOLVER_TITLE, AI_SOLVING_MSG)
        
        # Try BFS first (optimal solution)
        solution = self._solver.solve_bfs()
        
        if solution is None:
            messagebox.showwarning(AI_SOLVER_TITLE, AI_NO_SOLUTION_MSG)
            self._solving = False
            return
        
        if len(solution) == 0:
            messagebox.showinfo(AI_SOLVER_TITLE, AI_ALREADY_SOLVED_MSG)
            self._solving = False
            return
        
        # Show solution step by step
        self._solution = solution
        messagebox.showinfo(AI_SOLVER_TITLE, AI_SOLUTION_FOUND_MSG.format(len(solution)))
        self._play_solution()
    
    def _get_hint(self) -> None:
        """Get the next move hint from AI solver."""
        solution = self._solver.solve_bfs()
        
        if solution is None:
            messagebox.showwarning(AI_HINT_TITLE, AI_NO_SOLUTION_MSG)
            return
        
        if len(solution) == 0:
            messagebox.showinfo(AI_HINT_TITLE, AI_ALREADY_SOLVED_MSG)
            return
        
        # Show first move as hint using unified movement system
        first_move = solution[0]
        direction_name = next((name for name, info in MOVE_DIRECTIONS.items() 
                              if info['delta'] == first_move), 'UNKNOWN')
        messagebox.showinfo(AI_HINT_TITLE, AI_TRY_MOVING_MSG.format(direction_name))
    
    def _play_solution(self) -> None:
        """Play the AI solution step by step with delays."""
        if not self._solution:
            self._solving = False
            return
        
        if len(self._solution) == 0:
            messagebox.showinfo(AI_SOLVER_TITLE, AI_SOLUTION_COMPLETE_MSG)
            self._solving = False
            return
        
        # Execute next move
        next_move = self._solution.pop(0)
        self._model.move_cat(next_move)
        self._redraw()
        
        # Check if puzzle is solved
        if self._model.room_messed():
            messagebox.showinfo(AI_SOLVER_TITLE, AI_PUZZLE_SOLVED_MSG)
            self._solving = False
            return
        
        # Schedule next move
        self._root.after(1000, self._play_solution)  # 1 second delay
