from constants import *
import os


class BasicTile:
    _text = EMPTY

    def __init__(self) -> None:
        self._passable = True

    def is_passable(self) -> bool:
        return self._passable

    def get_text(self) -> str:
        return self._text


class Empty(BasicTile):
    def __init__(self) -> None:
        super().__init__()


class Wall(BasicTile):
    _text = WALL

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
    _text = DEST

    def __init__(self) -> None:
        super().__init__()
        self._filled = False


class MoveableEntity:
    _text = '_'

    def __init__(self, pos: tuple[int, int]) -> None:
        self._row, self._col = pos

    def get_text(self) -> str:
        return self._text

    def get_pos(self) -> tuple[int, int]:
        return self._row, self._col

    def move(self, delta: tuple[int, int]) -> None:
        self._row += delta[0]
        self._col += delta[1]


class Glass(MoveableEntity):
    _text = GLASS

    def __init__(self, pos: tuple[int, int]) -> None:
        super().__init__(pos)


class Cat(MoveableEntity):
    _text = CAT

    def __init__(self,
                 pos: tuple[int, int],
                 max_tiredness: int = DEFAULT_TIREDNESS):
        super().__init__(pos)
        self._max_tiredness = max_tiredness
        self._tiredness = 0

    def is_tired(self) -> bool:
        return self._tiredness > self._max_tiredness


class Playground:
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

    def move_glass(self, box: Glass, delta: tuple[int, int]) -> None:
        del self._glasses[box.get_pos()]
        box.move(delta)
        self._glasses[box.get_pos()] = box

    def update_dests(self) -> None:
        for k in self._dest_filled:
            self._dest_filled[k] = True if k in self._glasses else False

    def all_filled(self) -> bool:
        return all(self._dest_filled.values())

    def tile_passable(self, row: int, col: int) -> bool:
        return self._tiles[row][col].is_passable()


class Model:
    def __init__(self, game_dir: str):

        self._game_dir = game_dir
        self._playground = os.listdir(self._game_dir)
        self._num_playgrounds = len(self._playground)
        self._cur_lv = 0
        self._cur_playground = None
        self._cat = None
        self.load_game()

    def load_game(self) -> None:
        with open(os.path.join(os.getcwd(), self._game_dir, self._playground[self._cur_lv])) as tiles:
            cols = []
            for col in tiles:
                cols.append(col.strip('\n'))
            num_rows, num_cols = len(cols), len(cols[0])
            playground = Playground(num_rows, num_cols)
            playground.set_playground(cols)
            self._cat = Cat(playground.get_cat_start())
            self._cur_playground = playground

    def set_cat(self, player_pos: tuple[int, int]) -> None:
        self._cat = Cat(player_pos)

    def get_num_playgrounds(self) -> int:
        return self._num_playgrounds

    def get_cur_lv(self) -> int:
        return self._cur_lv

    def get_cat(self) -> Cat:
        return self._cat

    def get_playground(self) -> Playground:
        return self._cur_playground

    def level_up(self) -> None:
        self._cur_lv += 1
        self.load_game()

    def playground_messed(self) -> bool:
        return self._cur_playground.all_filled()

    def attempt_push_glass(self, box: Glass, delta: tuple[int, int]) -> None:
        row, col = box.get_pos()
        target_row, target_col = row + delta[0], col + delta[1]
        if self._cur_playground.tile_passable(target_row, target_col) and \
                (target_row, target_col) not in self._cur_playground.get_glasses() and \
                self.within_boundary(target_row, target_col):
            self._cur_playground.move_glass(box, delta)
            self._cur_playground.update_dests()
            return True
        return False

    def within_boundary(self, row: int, col: int) -> bool:
        max_row, max_col = self._cur_playground.get_dimension()
        if row < 0 or col < 0 or row >= max_row or col >= max_col:
            return False
        return True

    def move_cat(self, delta: tuple[int, int]) -> None:
        cur_row, cur_col = self._cat.get_pos()
        target_row, target_col = cur_row + delta[0], cur_col + delta[1]
        target_tile = self._cur_playground.get_tile(target_row, target_col)

        if (not self.within_boundary(target_row, target_col)) or (not target_tile.is_passable()):
            return

        # move glass and the cat
        if (target_row, target_col) in self._cur_playground.get_glasses().keys():
            if self.attempt_push_glass(self._cur_playground.get_glass(target_row, target_col), delta):
                self._cat.move(delta)
        else:
            self._cat.move(delta)
