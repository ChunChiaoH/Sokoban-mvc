from constants import *
import os


class BasicTile:
    _symbol = EMPTY

    def __init__(self) -> None:
        self._passable = True

    def is_passable(self) -> bool:
        return self._passable

    def get_text(self) -> str:
        return self._symbol


class Empty(BasicTile):
    def __init__(self) -> None:
        super().__init__()


class Wall(BasicTile):
    _symbol = WALL

    def __init__(self) -> None:
        super().__init__()
        self._passable = False


class Exit(Wall):
    def __init__(self) -> None:
        super().__init__()

    def open(self) -> None:
        self._passable = True
        self._text = EMPTY


class Dest(BasicTile):
    _symbol = DEST

    def __init__(self) -> None:
        super().__init__()
        self._filled = False


class MoveableEntity:
    _symbol = MOVEABLE_ENTITY

    def __init__(self, pos: tuple[int, int]) -> None:
        self._row, self._col = pos

    def get_text(self) -> str:
        return self._symbol

    def get_pos(self) -> tuple[int, int]:
        return self._row, self._col

    def move(self, delta: tuple[int, int]) -> None:
        self._row += delta[0]
        self._col += delta[1]


class Glass(MoveableEntity):

    def __init__(self, pos: tuple[int, int]) -> None:
        super().__init__(pos)
        self._symbol = GLASS

    def broken(self) -> None:
        self._symbol = BROKEN_GLASS

    def unbroken(self) -> None:
        self._symbol = GLASS


class Cat(MoveableEntity):
    _symbol = CAT

    def __init__(self,
                 pos: tuple[int, int],
                 max_tiredness: int = DEFAULT_TIREDNESS):
        super().__init__(pos)
        self._max_tiredness = max_tiredness
        self._tiredness = 0

    def is_tired(self) -> bool:
        return self._tiredness > self._max_tiredness


class Room:
    TILES = {WALL: Wall, EMPTY: Empty, DEST: Dest}

    def __init__(self, row: int, col: int) -> None:
        self._dimension = (row, col)
        self._tiles = []
        self._dest_filled = {}
        self._glasses = {}
        self._cat_start = None

    def set_playground(self, tiles: list[str]):
        self._tiles = [[self.TILES.get(tile, Empty)()
                        for tile in row] for row in tiles]
        self._dest_filled = {(i, j): False
                             for i, row in enumerate(tiles) for j, col in enumerate(row) if col == DEST}
        self._glasses = {(i, j): Glass((i, j))
                         for i, row in enumerate(tiles) for j, col in enumerate(row) if col == GLASS}
        self._cat_start = [(i, j)
                           for i, row in enumerate(tiles) for j, col in enumerate(row) if col == CAT][0]

    def get_dimension(self) -> tuple[int, int]:
        return self._dimension

    def get_cat_start(self) -> tuple[int, int]:
        return self._cat_start

    def get_glasses(self) -> dict[tuple[int, int]: Glass]:
        return self._glasses

    def get_glass(self, row: int, col: int) -> Glass:
        return self._glasses[(row, col)]

    def get_tile(self, row: int, col: int) -> str:
        return self._tiles[row][col]

    def get_tiles(self) -> list[list[BasicTile]]:
        return self._tiles

    def move_glass(self, box: Glass, delta: tuple[int, int]) -> None:
        del self._glasses[box.get_pos()]
        box.move(delta)
        self._glasses[box.get_pos()] = box

    def update_dests(self) -> None:
        for k in self._dest_filled:
            self._dest_filled[k] = True if k in self._glasses else False
        for k in self._glasses:
            if k in self._dest_filled:
                self._glasses[k].broken()
            else:
                self._glasses[k].unbroken()

    def all_filled(self) -> bool:
        return all(self._dest_filled.values())

    def tile_passable(self, row: int, col: int) -> bool:
        return self._tiles[row][col].is_passable()


class Model:
    def __init__(self, game_dir: str):

        self._game_dir = game_dir
        self._rooms = os.listdir(self._game_dir)
        self._num_rooms = len(self._rooms)
        self._cur_room_num = 0
        self._cur_room = None
        self._cat = None
        self.load_game()

    def load_game(self) -> None:
        with open(os.path.join(os.getcwd(), self._game_dir, self._rooms[self._cur_room_num])) as tiles:
            cols = []
            for col in tiles:
                cols.append(col.strip('\n'))
            num_rows, num_cols = len(cols), len(cols[0])
            room = Room(num_rows, num_cols)
            room.set_playground(cols)
            self._cat = Cat(room.get_cat_start())
            self._cur_room = room

    def set_cat(self, cat_pos: tuple[int, int]) -> None:
        self._cat = Cat(cat_pos)

    def get_num_rooms(self) -> int:
        return self._num_rooms

    def get_cur_room_num(self) -> int:
        return self._cur_room_num

    def get_cat(self) -> Cat:
        return self._cat

    def get_room(self) -> Room:
        return self._cur_room

    def level_up(self) -> None:
        self._cur_room_num += 1
        self.load_game()

    def room_messed(self) -> bool:
        return self._cur_room.all_filled()

    def attempt_push_glass(self, glass: Glass, delta: tuple[int, int]) -> None:
        row, col = glass.get_pos()
        target_row, target_col = row + delta[0], col + delta[1]
        if self._cur_room.tile_passable(target_row, target_col) and \
                (target_row, target_col) not in self._cur_room.get_glasses() and \
                self.within_boundary(target_row, target_col):
            self._cur_room.move_glass(glass, delta)
            self._cur_room.update_dests()
            return True
        return False

    def within_boundary(self, row: int, col: int) -> bool:
        max_row, max_col = self._cur_room.get_dimension()
        if row < 0 or col < 0 or row >= max_row or col >= max_col:
            return False
        return True

    def move_cat(self, delta: tuple[int, int]) -> None:
        cur_row, cur_col = self._cat.get_pos()
        target_row, target_col = cur_row + delta[0], cur_col + delta[1]
        target_tile = self._cur_room.get_tile(target_row, target_col)

        if (not self.within_boundary(target_row, target_col)) or (not target_tile.is_passable()):
            return

        # move glass and the cat
        if (target_row, target_col) in self._cur_room.get_glasses().keys():
            if self.attempt_push_glass(self._cur_room.get_glass(target_row, target_col), delta):
                self._cat.move(delta)
        else:
            self._cat.move(delta)
