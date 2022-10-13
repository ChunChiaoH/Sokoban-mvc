DEST = '0'
WALL = '+'
EMPTY = ' '
BOX = 'B'
WORKER = 'W'

UP = 'w'
DOWN = 's'
LEFT = 'a'
RIGHT = 'd'
MOVES = {
    UP: (-1, 0),
    DOWN: (1, 0),
    LEFT: (0, -1),
    RIGHT: (0, 1),
}

END_GAME = 'end'

DEFAULT_TIREDNESS = 1000

PROMPT_TEXT = 'Enter a move(w,a,s,d) or "end" to quit:'
DEFAULT_GAMES = 'games/default'
DIR_NOT_EXIST = 'Directory does not exist, play default games.'
PRESS_ANY = 'Press any key to continue.'
GAMEFILE_TEXT = 'Enter game directory:'
WIN = 'Win! All storehouses are finished.'
