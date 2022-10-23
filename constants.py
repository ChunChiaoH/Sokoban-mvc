DEST = '0'
WALL = '+'
EMPTY = ' '
GLASS = 'G'
BROKEN_GLASS = 'B'
CAT = 'C'
MOVEABLE_ENTITY = '_'

#UP = 'w'
#DOWN = 's'
#LEFT = 'a'
#RIGHT = 'd'

UP=87 #'w'
UP_ARROW=38

DOWN=83 #'s'
DOWN_ARROW = 40

LEFT = 65 #'d'
LEFT_ARROW = 37

RIGHT = 68 #'a'
RIGHT_ARROW = 39

ARROWS = {}
MOVE_CODES = {
    UP: (-1, 0),
    UP_ARROW: (-1, 0),
    DOWN: (1, 0),
    DOWN_ARROW: (1, 0),
    LEFT: (0, -1),
    LEFT_ARROW: (0, -1),
    RIGHT: (0, 1),
    RIGHT_ARROW: (0, 1)
}

END_GAME = 'end'

DEFAULT_TIREDNESS = 1000

TITLE = 'SOKOBAN'
PROMPT_TEXT = 'Enter a move(w,a,s,d) or "end" to quit:'
DEFAULT_GAMES = 'games/default'
DIR_NOT_EXIST = 'Directory does not exist, play default games.'
PRESS_ANY = 'The room is messed. Press any key to continue.'
GAMEFILE_TEXT = 'Enter game directory:'
WIN_TITLE = 'Won!'
WIN = 'Miao! All rooms are messed.'
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
ROOM_CANVAS_WIDTH, ROOM_CANVAS_HEIGHT = 600, 600
KEY_EVENT = "<Key>"

IMAGE_FOLDER = 'images/'
TILE_IMAGES = {
    WALL: 'wall.png',
    EMPTY: 'empty.png',
    DEST: 'dest.png'
}

MOVEABLE_ENTITY_IMAGES = {
    CAT: 'cat.png',
    GLASS: 'glass.png',
    BROKEN_GLASS: 'broken_glass.png'
}
