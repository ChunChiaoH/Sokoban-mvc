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


class Box(MoveableEntity):
    _text = BOX

    def __init__(self, pos: tuple[int, int]) -> None:
        super().__init__(pos)


class Worker(MoveableEntity):
    _text = WORKER

    def __init__(self,
                 pos: tuple[int, int],
                 max_tiredness: int = DEFAULT_TIREDNESS):
        super().__init__(pos)
        self._max_tiredness = max_tiredness
        self._tiredness = 0

    def is_tired(self) -> bool:
        return self._tiredness > self._max_tiredness


class Storehouse:
    TILES = {WALL: Wall, EMPTY: Empty, DEST: Dest}

    def __init__(self, row: int, col: int) -> None:
        self._dimension = (row, col)
        self._tiles = []
        self._dest_filled = {}
        self._boxes = {}
        self._worker_start = None

    def set_storehouse(self, tiles: list[str]):
        self._tiles = [[self.TILES.get(tile, Empty)()
                        for tile in row] for row in tiles]
        self._dest_filled = {(i, j): False
                             for i, row in enumerate(tiles) for j, col in enumerate(row) if col == DEST}
        self._boxes = {(i, j): Box((i, j))
                       for i, row in enumerate(tiles) for j, col in enumerate(row) if col == BOX}
        self._worker_start = [(i, j)
                              for i, row in enumerate(tiles) for j, col in enumerate(row) if col == WORKER][0]

    def get_dimension(self) -> tuple[int, int]:
        return self._dimension

    def get_worker_start(self) -> tuple[int, int]:
        return self._worker_start

    def get_boxes(self) -> dict[tuple[int, int]: Box]:
        return self._boxes

    def get_box(self, row: int, col: int) -> Box:
        return self._boxes[(row, col)]

    def get_tile(self, row: int, col: int) -> str:
        return self._tiles[row][col]

    def move_box(self, box: Box, delta: tuple[int, int]) -> None:
        del self._boxes[box.get_pos()]
        box.move(delta)
        self._boxes[box.get_pos()] = box

    def update_dests(self) -> None:
        for k in self._dest_filled:
            self._dest_filled[k] = True if k in self._boxes else False

    def all_filled(self) -> bool:
        return all(self._dest_filled.values())

    def tile_passable(self, row: int, col: int) -> bool:
        return self._tiles[row][col].is_passable()


class Model:
    def __init__(self, game_dir: str):

        self._game_dir = game_dir
        self._storehouses = os.listdir(self._game_dir)
        self._num_storehouses = len(self._storehouses)
        self._cur_lv = 0
        self._cur_storehouse = None
        self._worker = None
        self.load_game()

    def load_game(self) -> None:
        with open(os.path.join(os.getcwd(), self._game_dir, self._storehouses[self._cur_lv])) as tiles:
            cols = []
            for col in tiles:
                cols.append(col.strip('\n'))
            num_rows, num_cols = len(cols), len(cols[0])
            storehouse = Storehouse(num_rows, num_cols)
            storehouse.set_storehouse(cols)
            self._worker = Worker(storehouse.get_worker_start())
            self._cur_storehouse = storehouse

    def set_player(self, player_pos: tuple[int, int]) -> None:
        self._worker = Worker(player_pos)

    def get_num_storehouses(self) -> int:
        return self._num_storehouses

    def get_cur_lv(self) -> int:
        return self._cur_lv

    def get_worker(self) -> Worker:
        return self._worker

    def get_storehouse(self) -> Storehouse:
        return self._cur_storehouse

    def level_up(self) -> None:
        self._cur_lv += 1
        self.load_game()

    def storehouse_finished(self) -> bool:
        return self._cur_storehouse.all_filled()

    def attempt_push_box(self, box: Box, delta: tuple[int, int]) -> None:
        row, col = box.get_pos()
        target_row, target_col = row + delta[0], col + delta[1]
        if self._cur_storehouse.tile_passable(target_row, target_col) and \
                (target_row, target_col) not in self._cur_storehouse.get_boxes() and \
                self.within_boundary(target_row, target_col):
            self._cur_storehouse.move_box(box, delta)
            self._cur_storehouse.update_dests()
            return True
        return False

    def within_boundary(self, row: int, col: int) -> bool:
        max_row, max_col = self._cur_storehouse.get_dimension()
        if row < 0 or col < 0 or row >= max_row or col >= max_col:
            return False
        return True

    def move_worker(self, delta: tuple[int, int]) -> None:
        cur_row, cur_col = self._worker.get_pos()
        target_row, target_col = cur_row + delta[0], cur_col + delta[1]
        target_tile = self._cur_storehouse.get_tile(target_row, target_col)

        if (not self.within_boundary(target_row, target_col)) or (not target_tile.is_passable()):
            return

        # move box and the worker
        if (target_row, target_col) in self._cur_storehouse.get_boxes().keys():
            if self.attempt_push_box(self._cur_storehouse.get_box(target_row, target_col), delta):
                self._worker.move(delta)
        else:
            self._worker.move(delta)
