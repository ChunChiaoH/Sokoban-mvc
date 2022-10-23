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


class RoomCanvas(tk.Canvas):
    def __init__(
            self,
            master: Union[tk.Tk, tk.Frame],
            dimension: tuple[int, int],
            width: int,
            height: int,
            **kwargs
    ) -> None:
        super().__init__(
            master,
            width=width,
            height=height,
            **kwargs
        )
        self._tile_imgs = None
        self._entity_imgs = None
        self._dimension = dimension
        self.width, self.height = width, height
        self._img_size = int(width / dimension[1]), int(height / dimension[0])
        self._tile_imgs = None
        self._entity_imgs = None
        self.update_imgs()

    def draw(self, cat: Cat, room: Room) -> None:
        glasses = room.get_glasses()
        for i, row in enumerate(room.get_tiles()):
            for j, tile in enumerate(row):
                img = self._tile_imgs[tile.get_text()]
                self._draw_img((i, j), img)
                if (i, j) in glasses:
                    img = self._entity_imgs[glasses[(i, j)].get_text()]
                    self._draw_img((i, j), img)
        self._draw_img(cat.get_pos(), self._entity_imgs[CAT])

        self.update()

    def clear(self) -> None:
        for w in self.winfo_children():
            w.destroy()

    def get_img_center(self, position: tuple[int, int]) -> tuple[int, int]:
        width, height = self.get_img_size()
        x_center, y_center = int(position[1]*width + width/2), int(position[0]*height + height/2)
        return x_center, y_center

    def update_imgs(self) -> None:
        self.update_img_size()
        self._tile_imgs = self._load_imgs(TILE_IMAGES)
        self._entity_imgs = self._load_imgs(MOVEABLE_ENTITY_IMAGES)

    def _load_imgs(self, img_paths: dict[str: str]) -> dict[str: tk.Image]:
        return {name: ImageTk.PhotoImage(
        Image.open(IMAGE_FOLDER + path).resize(self._img_size))
                         for name, path in img_paths.items()}

    def set_dimension(self, dimension: tuple[int, int]) -> None:
        self._dimension = dimension

    def get_img_size(self) -> tuple[int, int]:
        return self._img_size

    def update_img_size(self) -> None:
        num_rows, num_cols = self._dimension
        self._img_size = int(self.width / num_cols), int(self.height / num_rows)

    def _draw_img(self, pos: tuple[int, int], img: ImageTk) -> None:
        x_center, y_center = self.get_img_center(pos)
        self.create_image(x_center, y_center, image=img)


class GraphicalView:
    def __init__(self, master: tk.Tk) -> None:
        self._master = master
        self._master.geometry("")
        self._master.title(TITLE)
        self._master.resizable(tk.FALSE, tk.FALSE)

        self._all_frames = tk.Frame(self._master)
        self._all_frames.pack()
        self._room_frame = tk.Frame(self._all_frames)
        self._room_frame.pack()
        self._room_canvas = None
        self._room_dimension = None

    def clear_canvases(self) -> None:
        for frame in self._all_frames.winfo_children():
            for canvas in frame.winfo_children():
                canvas.clear()

    def create_components(self, dimension) -> None:
        self._room_dimension = dimension
        self._room_canvas = RoomCanvas(self._room_frame, self._room_dimension, ROOM_CANVAS_WIDTH, ROOM_CANVAS_HEIGHT)
        self._room_canvas.pack()

    def bind_keyboard_callback(self, command: Callable[[tk.Event], None]) -> None:
        self._master.bind(KEY_EVENT, command)

    def draw(self, cat: Cat, room: Room) -> None:
        self.clear_canvases()
        self._room_canvas.draw(cat, room)

    def set_room_dimension(self, dimension: tuple[int, int]) -> None:
        self._room_canvas.set_dimension(dimension)

    def update_canvas_imgs(self) -> None:
        self._room_canvas.update_imgs()


